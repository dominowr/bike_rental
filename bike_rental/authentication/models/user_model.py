from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\d{9}$',
        message='Phone no. must consist of exactly 9 digits.'
    )

    verify_token = models.UUIDField(max_length=255, unique=True, blank=True, null=True)
    phone_no = models.CharField(validators=[phone_regex], blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username
