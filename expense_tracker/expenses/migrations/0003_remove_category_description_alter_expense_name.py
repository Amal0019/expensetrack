# Generated by Django 5.1.5 on 2025-01-22 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_expense_name_alter_expense_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
        migrations.AlterField(
            model_name='expense',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
