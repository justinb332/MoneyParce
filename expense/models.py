from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.conf import settings
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expenses",
    )

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or slugify(self.name) != self.slug:
            base_slug = slugify(self.name) or get_random_string(8)
            slug = base_slug
            count = 1

            while Expense.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1

            self.slug = slug

        super().save(*args, **kwargs)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('expense.Category', on_delete=models.CASCADE, null=True)

    date = models.DateTimeField(default=timezone.now)

    notes = models.TextField(null=True, blank=True)

    is_recurring = models.BooleanField(default=False)
    recurrence_period = models.CharField(
        max_length=10,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
        ],
        null=True,
        blank=True
    )
    recurrence_day_of_week = models.CharField(
        max_length=10,
        choices=[
            ('monday', 'Monday'),
            ('tuesday', 'Tuesday'),
            ('wednesday', 'Wednesday'),
            ('thursday', 'Thursday'),
            ('friday', 'Friday'),
            ('saturday', 'Saturday'),
            ('sunday', 'Sunday'),
        ],
        null=True,
        blank=True
    )
    recurrence_day_of_month = models.PositiveIntegerField(null=True, blank=True)
    next_occurrence = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} (${self.amount})"
