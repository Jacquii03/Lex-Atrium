from django.db import models
from django.contrib.auth import  get_user_model
from caseManagement.models import Case



User = get_user_model()


class Calendar(models.Model):
    case = models.ForeignKey(Case, on_delete=models.PROTECT)
    schedule = models.CharField(max_length=5000)
    schedule_time = models.TimeField()
    schedule_date = models.DateField()
    schedule_creator = models.ForeignKey(User, on_delete=models.PROTECT)