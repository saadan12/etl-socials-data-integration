from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..managers.customUser import UsersManager


class Users(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    user_type = models.ForeignKey(
        'User_Type', on_delete=models.SET_NULL, null=True)
    account = models.ForeignKey(
        'Account', on_delete=models.SET_NULL, null=True)
    email = models.EmailField(_('email address'), unique=True, blank=False)
    password = models.TextField(max_length=255, blank=False)
    name = models.CharField(max_length=50, blank=False, null=True)
    surname = models.CharField(max_length=50, blank=False, null=True)
    phone = models.CharField(max_length=17, blank=True)
    photo = models.CharField(max_length=255, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_emailMarketing = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now=True)
    stripe_endDate = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(default=timezone.now)
    stripe_id = models.BigIntegerField(blank=True, null=True)
    stripe_isActive = models.BooleanField(default=False)
    stripe_endDate = models.DateTimeField(auto_now=True)
    stripe_subscriptionID = models.BigIntegerField(
        blank=True, null=True)
    stripe_subscriptionPlan = models.CharField(max_length=255)
    is_termsOfServicePrivacyPolicy = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UsersManager()
