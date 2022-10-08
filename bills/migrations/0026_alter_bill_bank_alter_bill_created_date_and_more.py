# Generated by Django 4.1.1 on 2022-10-08 01:09

import bills.models
import bills.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0025_remove_bill_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='bank',
            field=models.CharField(blank=True, choices=[('BANCO_DO_BRASIL', 'Banco do Brasil'), ('BANCO_CORA', 'Banco Cora'), ('BRADESCO', 'Bradesco'), ('CAIXA', 'Caixa'), ('ITAU', 'Itaú'), ('ITI', 'Iti'), ('MERCADO_PAGO', 'Mercado Pago'), ('NUBANK', 'Nubank'), ('PAG_SEGURO', 'Pag Seguro'), ('PAY_PAL', 'Pay Pal'), ('PIC_PAY', 'Pic Pay'), ('SANTANDER', 'Santander'), ('OTHER', 'Outro')], max_length=30, null=True, verbose_name='Banco'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='created_date',
            field=models.DateField(default=bills.models.get_today_default_value, verbose_name='Data de Criação'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='days_to_notify_before_expiration',
            field=models.IntegerField(default=14, validators=[bills.validators.only_positive_numbers], verbose_name='Dias para Notificar Antes do Vencimento'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='expiration_date',
            field=models.DateField(blank=True, null=True, verbose_name='Data de Vencimento'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='installment_sequence',
            field=models.IntegerField(blank=True, default=1, null=True, validators=[bills.validators.only_greater_than_zero], verbose_name='Número da Parcela'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='installment_total',
            field=models.IntegerField(blank=True, null=True, validators=[bills.validators.only_greater_than_zero], verbose_name='Quantidade de Parcelas'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='payment_date',
            field=models.DateField(blank=True, null=True, validators=[bills.validators.only_date_lower_or_equal_today], verbose_name='Data de Pagamento'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='payment_proof_file',
            field=models.FileField(blank=True, null=True, upload_to=bills.models.get_payment_proof_path, validators=[bills.validators.payment_proof_file_size_validator, bills.validators.payment_proof_file_format_validator], verbose_name='Comprovante de Pagamento'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='payment_type',
            field=models.CharField(blank=True, choices=[('MONEY', 'Dinheiro'), ('DEBIT', 'Débito'), ('CREDIT', 'Crédito'), ('PIX', 'Pix'), ('ONLINE', 'Online'), ('TRANSFER', 'Transferência')], max_length=18, null=True, verbose_name='Forma de Pagamento'),
        ),
    ]
