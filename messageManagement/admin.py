from django.contrib import admin
from .models import Message,UserMessage

# Register your models here.
admin.site.register(Message)
admin.site.register(UserMessage)