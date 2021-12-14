from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# THis class reconfigures the inbuilt user data to 
# my own custom user detail
class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email,  password, **other_fields)

    def create_user(self, email, password, **other_fields):
        
        other_fields.setdefault('is_active', True)

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user





# New Custom User Table rows
class User(AbstractBaseUser, PermissionsMixin):
    
    
    ROLES = (
        ('chief judge','Chief Judge'),
        ('judge','Judge'),
        ('lawyer','Lawyer'),
        ('litigant','Litigant'),
    )

    email = models.EmailField(_('email address'), unique=True, null=False, blank=False)
    call_to_bar_number = models.CharField(max_length=150, unique=True,null=True, blank=True)
    court = models.CharField(max_length=150, null=True, blank=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=150,)
    last_name = models.CharField(max_length=150,)
    role = models.CharField(max_length=150,choices=ROLES,null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, null=False, blank=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name',"last_name","role","call_to_bar_number"]

    def __str__(self):
        return self.email
    



class ForgotPassword(models.Model):
    email = models.EmailField(_('email address'), unique=True, null=False, blank=False)
    token = models.IntegerField()

