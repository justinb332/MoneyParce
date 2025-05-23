# Generated by Django 5.1.5 on 2025-04-08 08:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('income', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categories',
            new_name='Category',
        ),
        migrations.AlterField(
            model_name='income',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='income.category'),
        ),
        migrations.AlterField(
            model_name='income',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
