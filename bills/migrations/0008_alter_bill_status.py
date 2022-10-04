# Generated by Django 4.1.1 on 2022-10-04 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0007_rename_create_date_bill_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='status',
            field=models.CharField(choices=[('UNDEFINED', 'INDEFINIDO'), ('TO_EXPIRE', 'A VENCER'), ('EXPIRED', 'EXPIRADA'), ('WARNING', 'ATENÇÃO'), ('PAID', 'PAGA')], default='UNDEFINED', max_length=9),
        ),
    ]
