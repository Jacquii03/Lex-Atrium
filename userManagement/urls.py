from django.urls import path, include
# import funtipons from the views
from .views import register,index,login,logout_view,proffessional_info,settings,forgot_password,forgot_email


# Setting the url routes from the view for this app
urlpatterns = [
    path('', index),
    path('accounts/signup/', register),
    path('login/', login),
    path('forgot^password/', forgot_password),
    path('forgot^email/', forgot_email),
    path('logout/', logout_view),
    path('settings/', settings),
    path('accounts/p^info/', proffessional_info, name="pinfo"),
]