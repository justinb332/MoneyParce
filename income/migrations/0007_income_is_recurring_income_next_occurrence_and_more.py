# Generated by Django 5.2 on 2025-04-22 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('income', '0006_alter_income_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='is_recurring',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='income',
            name='next_occurrence',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='income',
            name='recurrence_day_of_month',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='income',
            name='recurrence_day_of_week',
            field=models.CharField(blank=True, choices=[('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='income',
            name='recurrence_period',
            field=models.CharField(blank=True, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], max_length=10, null=True),
        ),
    ]
