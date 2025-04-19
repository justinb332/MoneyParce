from django.db import models
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Income(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwards):
        base_slug = slugify(self.name)
        slug = base_slug
        count = 1

        while Income.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1

        self.slug = slug
        super().save(*args, **kwards)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('income.Category', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.amount} - {self.category.name} ({self.amount})"

