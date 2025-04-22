from django.db import models
from accounts.models import CustomUser


class Report(models.Model):
    user = models.ForeignKey(CustomUser, related_name="report_set", on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Report for {self.user.username}"
