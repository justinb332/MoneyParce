# Generated by Django 5.1.5 on 2025-04-08 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('income', '0003_alter_income_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
