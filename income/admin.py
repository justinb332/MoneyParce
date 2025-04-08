from django.contrib import admin
from .models import Income, Category


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    # Customize the fields displayed in the list view of the admin panel
    list_display = ('name', 'amount', 'category', 'date', 'notes')
    search_fields = ('name', 'category__name')  # Allow searching by name and category
    list_filter = ('category', 'date')  # Add filters for category and date


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

