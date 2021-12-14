from django.urls import path, include
from .views import calendar,delete_calendar


app_name = "calendar_urls"
urlpatterns = [
    path('',calendar, name="calendar"),
    path('delete/<int:id>/^',delete_calendar, name="delete_calendar"),
    # path('create/new/^',new_message_view, name="new_message"),
]