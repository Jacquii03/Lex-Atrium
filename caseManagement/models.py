from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


STATUS = (
    ('not assigned', 'not assigned'),
    ('ongoing', 'ongoing'),
    ('archived', 'archived'),
)

CASE_TYPE = (
    ('criminal', 'criminal'),
    ('civil', 'civil'),
)


class Case(models.Model):
    name = models.CharField(max_length=150)
    case_type = models.CharField(max_length=100, choices=CASE_TYPE)
    status = models.CharField(
        max_length=150, choices=STATUS, default="not assigned")
    judge_assigned = models.CharField(max_length=150, default="Not assigned")
    judge_assigned_id = models.IntegerField(null=True, blank=True)
    court_assigned = models.CharField(max_length=200, default="Not assigned")
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    judgement = models.FileField(upload_to='judgement/', null=True, blank=True)



class CaseFolders(models.Model):
    case_file = models.FileField(upload_to='Case Files/')
    case_file_name = models.CharField(max_length=600)
    case = models.ForeignKey(Case, on_delete=models.PROTECT)
