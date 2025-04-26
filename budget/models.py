from django.db import models

# Create your models here.
# reports/models.py
from django.db import models
from django.contrib.auth.models import User

from expense.models import Category


class Budget(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Budget linked to a specific category
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Budgeted amount
    date_created = models.DateTimeField(auto_now_add=True)  # Timestamp


def __str__(self):
        return f"Budget for {self.category.name} - {self.total_amount}"

