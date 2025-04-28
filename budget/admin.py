# admin.py (Budget app)

from django.contrib import admin
from budget.models import Budget

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'category', 'timeframe')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'timeframe')
