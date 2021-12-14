from django.urls import path, include
from .views import new_message_view,message_view


app_name = "message_urls"
urlpatterns = [
    path('',message_view, name="message"),
    path('create/new/^',new_message_view, name="new_message"),
]