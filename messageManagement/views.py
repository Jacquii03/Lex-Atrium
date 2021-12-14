from django.shortcuts import render
from caseManagement.models import Case
from .models import Message, UserMessage
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

# Create your views here.

# reference to the User database object
User = get_user_model()

# this function returns the create message page
def new_message_view(request):
    # get all cases from the database
    case = Case.objects.all()
    # get all messages from the database
    msgObj = Message.objects.all()
    userMsgObj = UserMessage.objects.all()
    # checks if the http request is a post request
    if request.POST:
        # gets the values passed in the request object
        case_id = request.POST.get('case_id')
        title = request.POST.get('title')
        message = request.POST.get('message')
    # checks if the user is authenticated
        if 'user' not in request.session:
            user = request.user.id
        else:  
            user = request.session['user']
        # get the sender of the message from the database
        sender = User.objects.get(pk=user)
        # get the case object from the database
        case = Case.objects.get(pk=case_id)
        # save the message to the database
        msg = Message(title=title, message=message, case=case, sender=sender)
        msg.save()
        # return the message page
        return redirect('/message/')
    # return create message page
    return render(request, "newMessage.html", {'case': case,"msgs": msgObj, "userMsgs":userMsgObj})


# this function returns the message page with all messages
def message_view(request):
    # checks if the user is authenticated
    if 'user' in request.session:
        user = request.session['user']
    else:
        user = request.user.id
        # get all user message from database in descending order
    userMsgObj = UserMessage.objects.all().order_by('id')
    # mark message as read
    caseObj = Case.objects.filter(creator=user)
    for case in caseObj:
        Message.objects.filter(case=case).update(status="read")
    # end
    # gets a particular user id from a database
    userObj = User.objects.get(pk=user)
    # gets all case messages in descending order
    msgObj = Message.objects.all().order_by('-id')
    # return message web page
    return render(request, "message.html", {
        "msgs": msgObj,
        "user": userObj,
        "userMsgs":userMsgObj
    })
