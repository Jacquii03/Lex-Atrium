from django.db import models
from caseManagement.models import Case
from django.contrib.auth import  get_user_model


# reference to the User database object
User = get_user_model()




STATUS = (
        ('unread','unread'),
        ('read','read'),
)

# Case message database fields
class Message(models.Model):
    title = models.CharField(max_length=150)
    message = models.CharField(max_length=3050)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, default="unread", max_length=150)



# User message database fields
class UserMessage(models.Model):
    title = models.CharField(max_length=150)
    message = models.CharField(max_length=3050)
    receiver = models.IntegerField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, default="unread", max_length=150)