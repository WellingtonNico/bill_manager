# Generated by Django 4.1.1 on 2022-10-03 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0005_bill_note'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bill',
            options={'verbose_name': 'Conta', 'verbose_name_plural': 'Contas'},
        ),
    ]
