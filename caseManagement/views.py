from django.shortcuts import render
from .models import Case, CaseFolders
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from messageManagement.models import Message, UserMessage
from calendarManagement.models import Calendar

import os
from django.http import HttpResponse, Http404

# Create your views here.

# reference to the User database object
User = get_user_model()

# this function returns all the cases for a particular user
def case_view(request):
    # gets the current authenticated user from the browser cookies/session
    if request.user.is_authenticated:
        user = request.user.id
    else:
        user = request.session["user"]
    # gets the current user from the database
    userObj = User.objects.get(pk=user)
    # checks if user in request is a Chief Judge
    if userObj.role == "chief judge":
        # return all cases in descending order
        case = Case.objects.all().order_by('-id')
    # checks if user in request is a Judge
    elif userObj.role == "judge":
        # return all cases where Judge is assigned
        JoinedName = userObj.first_name + " "+userObj.last_name
        print(JoinedName)
        case = Case.objects.filter(judge_assigned=JoinedName).order_by('-pk')
    # checks if user in request is a normal litigant or lawyer
    else:
        # return all cases created by either lawyer or normal litigant
        case = Case.objects.filter(creator=user).order_by('-id')

    msgObj = Message.objects.all()
    return render(request, 'case.html', {"cases": case, "user": userObj,
                                         "msgs": msgObj,
                                         })


# Returns the new case details by ID template
def case_details_view(request, pk):

    # gets the current authenticated user from the browser cookies/session
    if "user" in request.session:
        user = request.session["user"]
    else:
        user = request.user.id

    # gets the current user from the database
    userObj = User.objects.get(pk=user)
    # gets all users from the database
    userAll = User.objects.all()
    # checks if id is in request
    if pk:
        # gets a case object based on the id
        case = Case.objects.get(pk=pk)
        # gets all case files based on the case returned
        caseFolder = CaseFolders.objects.filter(case=pk)

    # if the current request is a post request: gets the form data from the request
    if request.POST:
        # if user is a Chief Judge return all cases
        if userObj.role == "chief judge":

            #  gets the form data from the request
            judge_id = request.POST.get("judge_id")
            caseObj = Case.objects.filter(id=pk)
            judgeUser = User.objects.get(id=judge_id)
            judgeJoinedName = judgeUser.first_name + " "+judgeUser.last_name
            # updates the case object on the database with the Judge assigned
            caseObj.update(judge_assigned=judgeJoinedName, judge_assigned_id=judge_id,
                           court_assigned=judgeUser.court, status="ongoing")
            # updates the case object on the database with the court assigned
            courtObj = User.objects.get(court=judgeUser.court)
            # updates the database with the message about the assigned Judge and court 
            UserMessage(title="Case Assignment by Chief judge",
                        message=f'Case Number #{pk} has been assigned to you by the Chief Judge of the Federal Republic of Nigeria', receiver=courtObj.id, sender=userObj).save()

            Message(title="Case Approval",
                    message=f'Case Number #{pk} has been assigned a Judge', case=case, sender=userObj).save()
            # return case web page
            return redirect("/case/")

        # if user is a judge show case where judge is assigned to
        elif userObj.role == "judge":
            # check if request is a calendar schedule request
            isSchedule = request.POST.get('isSchedule')
            if isSchedule == 'true':
                stime = request.POST.get('stime')
                sdate = request.POST.get('sdate')
                schedule = "Court Hearing"
                # save hearing date and time in database
                cal = Calendar(case=case, schedule_date=sdate, schedule_time=stime,
                               schedule=schedule, schedule_creator=userObj).save()

                # save message notifying case participants of the schedule to database
                Message(title="Hearing Date Scheduled",
                        message=f'Case Number #{pk} has been Scheduled a date for hearing on {sdate} by {stime} ', case=case, sender=userObj).save()

            else:
                # get judgement file from request
                judgement = request.FILES["judgement_file"]
                caseObj = Case.objects.get(id=pk)
                # set case as archived
                caseObj.status = "archived"
                # set judgement for case
                caseObj.judgement = judgement
                # save case object
                caseObj.save()

                # save message notifying case participants of the uploaded judgement to database
                Message(title="Judgement Uploaded",
                        message=f'Case Number #{pk} has been Judged  and the judgement uploaded', case=case, sender=userObj).save()
            return redirect("/case/")

        # if user is a Litigant or lawyer, show cases created by them
        else:
            # check if request is a post request
            isUpdated = request.POST.get('isUpdated')
            # if update is true, update an uploaded case folder
            if isUpdated == "true":
                # gets the form data from the request
                updated_file = request.FILES.get('updated_file')
                caseFolderId = request.POST.get('caseFolderId')
                caseFold = CaseFolders.objects.get(pk=caseFolderId)
                caseFold.case = caseFold.case
                caseFold.case_file_name = caseFold.case_file_name
                caseFold.case_file = updated_file
                # save the new case folder
                caseFold.save()
                # redirect to the case detail page
                return redirect(f'/case/{pk}/detail/^')
            else:
                # get casefile from reuest
                filename = request.POST.get('filename')
                xfile = request.FILES['xfile']
                # save case file to database
                caseFolderss = CaseFolders(
                    case_file_name=filename, case=case, case_file=xfile)
                caseFolderss.save()
                # redirect to case details
                return redirect(f'/case/{pk}/detail/^')
    msgObj = Message.objects.all()
    return render(request, 'caseDetails.html', {"case": case, "casefolder": caseFolder, "user": userObj, "userall": userAll, "msgs": msgObj, })





# Returns the new case view template
def new_case_view(request):
    # gets the current authenticated user from the browser cookies/session
    if 'user' in request.session:
        user = request.session["user"]
    else:
        user = request.user.id
    userObj = User.objects.get(pk=user)
    cases = Case.objects.filter(creator=userObj)

    # if the current request is a post request: gets the form data from the request
    if request.POST:
        # gets the values passed in the request object
        case_type = request.POST.get("case_type")
        caseName = request.POST.get("case_name")
        if case_type == "both":
            Case(name=caseName, case_type="civil", creator=userObj).save()
            Case(name=caseName, case_type="criminal", creator=userObj).save()
        else:
            Case(name=caseName, case_type=case_type, creator=userObj).save()
        return redirect("/case/")
        # return render(request, 'case.html', {"message": "New case created","user":userObj,"cases":cases})
    msgObj = Message.objects.all()
    # return create case web page 
    return render(request, 'newCase.html', {"user": userObj, "msgs": msgObj, })







# this function downloads files from the database
def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(file_path)
            return response
    raise Http404
