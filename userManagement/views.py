from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from caseManagement.models import Case
from messageManagement.models import Message
from django.utils import timezone
from django.core.mail import send_mail
import random, math


# Create your views here.


# reference to the User database object
User = get_user_model()


# def generateOTP():
#     # Declare a digits variable 
#     # which stores all digits
#     digits = "0123456789"
#     OTP = ""
#    # length of password can be changed
#    # by changing value in range
#     for i in range(6) :
#         OTP += digits[math.floor(random.random() * 10)]
#     return OTP



# ////////////////////////////


# This function returns the registration page
# gets the form data from the post request(frontend) and creates a new user
def register(request):
    # checks if the http request is a post request
    if request.POST:
        # checks if the email entered already exists 
        email = request.POST.get('email')
        userObj = User.objects.filter(email=email).exists()
        if userObj == True:
            return render(request, "account/signup.html", {"message": "Email Already Exists"})
        else:
            # get all values passed in the post request of the submitted form
            firstName = request.POST.get('first_name')
            lastName = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password = make_password(password)

            # create new user by saving the details to the database
            userDetails = User(first_name=firstName,
                               last_name=lastName, email=email, password=password)
            userDetails.save()
            # set the user as an authenticated user
            request.session["user"] = userDetails.id
            # return complete registration web page
            return redirect('/accounts/p^info/')
    # return registration page
    return render(request, "account/signup.html", {})


# This function returns the daashboard page by
# checking if a user is authenticated and has completed registration
#  before redirecting to the dashboad(homepage)
def index(request):
# 
    # checks if the user is authenticated
    if request.user.is_authenticated:
        user = request.user.id
    elif "user" in request.session:
        user = request.session['user']
    else:
        return redirect('/login/')
    # gets the current authenticated user from the database
    userObj = User.objects.get(pk=user)
    # checks if the user completed registration by
    # checking if the user has a call to bar number and has selected a role
    if userObj.call_to_bar_number == "" or userObj.call_to_bar_number == None:
        return redirect('/accounts/p^info/')
    elif userObj.role == "" or userObj.role == None:
        return redirect('/accounts/p^info/')
    else:
        # gets all cases from database
        caseObj = Case.objects.all().order_by('-id')
        # gets all messages from database
        msgObj = Message.objects.all().order_by('-id')
        # creates a json object to return to the view
        context = {
            "user": userObj,
            "cases": caseObj,
            "msgs": msgObj
        }
        # returns the dashboard page
        return render(request, "dashboard.html", context)


# gets the form data from the post request(frontend)
#  and verifies if the user exists on the database by authentication
def login(request):
    if "success" in request.session:
        del request.session['success']
    # checks if the user is authenticated
    user = request.user
    if user.is_authenticated:
        if user.role != None or user.role != "":
            return redirect('/')
        return redirect('/accounts/p^info/')
    # checks if the http request is a post request
    if request.POST:
        # gets the values passed in the request object
        email = request.POST.get('email')
        password = request.POST.get('password')
        userData = authenticate(email=email, password=password)
        if userData is not None:
            request.session["user"] = userData.id
            return redirect('/')
        else:
            # returns the login page with an error
            return render(request, "account/login.html", {"error": "User doesn't exist"})
    # returns the login pagee
    return render(request, "account/login.html", {})


# signs out the current user
def logout_view(request):
    # removes the logged in user from the session//cookie
    if "user" in request.session:
        del request.session['user']
    logout(request)
    return redirect("/login/")


# updates the current registered user with their professional details
def proffessional_info(request):

    # gets the current authenticated user from the browser cookies/session
    if "user" in request.session:
        user = request.session['user']
    else:
        user = request.user.id
    # if the current request is a post request: gets the form data from the request
    if request.POST:
        # gets the values passed in the request object
        callToBarNumber = request.POST.get('call_to_bar_number')
        role = request.POST.get('role')
        court = request.POST.get('court')
        # checks if the user is a litigant and call to bar number
        if role == "litigant" and callToBarNumber == "":
            callToBarNumber = timezone.now()
        userDetails = User.objects.filter(id=user).update(
            call_to_bar_number=callToBarNumber, role=role, court=court)
        # redirects the user to the indexc
        return redirect("/")
    return render(request, "account/prof_info.html",)


# returns the settings webpage
def settings(request):
    # gets the current authenticated user from the browser cookies/session
    if "user" in request.session:
        user = request.session['user']
    else:
        user = request.user.id
    userObj = User.objects.get(pk=user)
    # if the current request is a post request: gets the form data from the request
    if request.POST:
         # gets the values passed in the request object
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        userObj.password = password
        userObj.save()
    # return settings web page
    return render(request, 'settings.html', {"user": userObj})


# def forgot_password(request):
#     if request.POST:
#         rtoken = request.POST.get('rtoken')
#         pword = request.POST.get('password')
#         fpword = ForgotPassword.objects.filter(token=rtoken)
#         if fpword.exists() == True:
#             fpword = ForgotPassword.objects.get(token=rtoken)
#             userObj = User.objects.get(email = fpword.email)
#             pword = make_password(pword)
#             userObj.password = pword
#             userObj.save()
#             fpword.delete()
#             return redirect("/login/")
#         else:
#             return render(request, "account/forgotPassword.html", {"error": "the token entered is incorrect"})
#     if 'success' in request.session:
#         return render(request, "account/forgotPassword.html",{"success":"success"})
#     else:
#         return render(request, "account/forgotPassword.html",{})

    
             
            

# def forgot_email(request):
#     if request.POST:
#         email = request.POST.get('email')
#         userObj = User.objects.filter(email=email).exists()
#         if userObj == False:
#             return render(request, "account/forgotEmail.html", {"error": "User with this email doesn't exist"})
#         else:
#             request.session['success'] = 'success'
#             email = request.POST.get('email')
#             token = generateOTP()

#             send_mail("Reset password on Lex-Atrium",f'your password token is {token}','ijeomaakwiwu@gmail.com',[email])
#             ForgotPassword(email=email, token=token).save()
#             return redirect("/forgot^password/")
#     return render(request, "account/forgotEmail.html", {})
        
