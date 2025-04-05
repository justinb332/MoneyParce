from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    security_question = models.TextField(max_length=255)
    security_answer = models.TextField(max_length=255)