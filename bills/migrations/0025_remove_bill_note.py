# Generated by Django 4.1.1 on 2022-10-07 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0024_alter_bill_days_to_notify_before_expiration_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='note',
        ),
    ]
