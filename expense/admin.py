from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Expense, Category


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'category', 'date', 'notes')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'date')
    fields = ('user', 'name', 'amount', 'category', 'date', 'notes',
              'is_recurring', 'recurrence_period',
              'recurrence_day_of_week', 'recurrence_day_of_month', 'next_occurrence')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
