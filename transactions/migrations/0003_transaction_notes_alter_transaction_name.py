# Generated by Django 5.1.5 on 2025-04-08 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_category_alter_transaction_date_transaction_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
