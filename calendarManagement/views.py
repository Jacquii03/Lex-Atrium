from django.shortcuts import render
from django.shortcuts import redirect
from .models import Calendar
from django.contrib.auth import get_user_model
from messageManagement.models import Message


User = get_user_model()

# return Calendar Schedule page
def calendar(request):
    # gets the current authenticated user from the browser cookies/session
    if 'user' in request.session:
        user = request.session['user']
    else:
        user = request.user.id
    # get all schedule from database
    calendarObj = Calendar.objects.all().order_by('-id')
    # get all messages from database
    msgObj = Message.objects.all().order_by('-id')
    # get user based on id in database
    userObj = User.objects.get(pk=user)

# if request in  post request  
    if request.POST:
        stime = request.POST.get('stime')
        sdate = request.POST.get('sdate')
        schedule = request.POST.get('schedule')
        userObj = User.objects.get(pk=user)
        cal = Calendar(schedule_date=sdate, schedule_time=stime,
                       schedule=schedule, schedule_creator=userObj)
        cal.save()
        return redirect('/calendar/')
    print(calendarObj)
    return render(request, 'calendar.html', {'calendar': calendarObj, "msgs": msgObj, "user": userObj})


def delete_calendar(request, pk):
    if pk:
        Calendar.objects.filter(pk=pk).delete()
    return render(request, 'calendar.html', {})



