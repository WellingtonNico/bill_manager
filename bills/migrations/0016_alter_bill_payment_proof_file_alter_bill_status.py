# Generated by Django 4.1.1 on 2022-10-05 17:34

import bills.models
import bills.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0015_alter_bill_payment_proof_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='payment_proof_file',
            field=models.FileField(blank=True, null=True, upload_to=bills.models.get_payment_proof_path, validators=[bills.validators.payment_proof_file_size_validator, bills.validators.payment_proof_file_format_validator], verbose_name='Comprovante de pagamento'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='status',
            field=models.CharField(choices=[('UNDEFINED', 'INDEFINIDO'), ('TO_EXPIRE', 'A VENCER'), ('EXPIRED', 'EXPIRADA'), ('EXPIRES_TODAY', 'VENCE HOJE'), ('WARNING', 'ATENÇÃO'), ('PAID', 'PAGA')], default='UNDEFINED', max_length=13),
        ),
    ]
