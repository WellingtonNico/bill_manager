# Generated by Django 4.1.1 on 2022-10-03 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0004_bill_days_to_notify_before_expiration'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='note',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Nota'),
        ),
    ]