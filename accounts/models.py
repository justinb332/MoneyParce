from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    security_question = models.TextField(max_length=255)
    security_answer = models.TextField(max_length=255)

    # 2FA Fields
    is_2fa_enabled = models.BooleanField(default=False)
    two_factor_secret = models.TextField(max_length=64, null=True, blank=True)
    two_factor_expiry = models.DateTimeField(null=True, blank=True)