# models.py (Budget app)
from datetime import timedelta

from django.db import models
from django.utils import timezone
from expense.models import Category, Expense  # Import Category model if needed


class Budget(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # Renamed from recurrence_type to timeframe
    timeframe = models.CharField(
        max_length=10,
        choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')]
    )

    # Add the unique constraint here to prevent duplicate category-timeframe combinations
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['category', 'timeframe'], name='unique_category_timeframe')
        ]

    def __str__(self):
        return f'{self.name} - {self.amount}'

    # Method to calculate total spent for different periods (daily, weekly, monthly)
    def total_spent(self, period):
        expenses = Expense.objects.filter(
            category=self.category,
            date__gte=self.get_date_range(period),  # Assume get_date_range handles period-based filtering
        )
        return sum(expense.amount for expense in expenses)

    def get_date_range(self, period):
        today = timezone.now().date()
        if period == 'daily':
            return today
        elif period == 'weekly':
            return today - timedelta(days=today.weekday())  # Start of the week (Monday)
        elif period == 'monthly':
            return today.replace(day=1)  # Start of the month
        return today
