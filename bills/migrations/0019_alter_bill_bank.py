# Generated by Django 4.1.1 on 2022-10-05 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0018_bill_bank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='bank',
            field=models.CharField(blank=True, choices=[('BANCO_DO_BRASIL', 'BANCO DO BRASIL'), ('BRADESCO', 'BRADESCO'), ('CAIXA', 'CAIXA'), ('ITAU', 'ITAÚ'), ('ITI', 'ITI'), ('MERCADO_PAGO', 'MERCADO PAGO'), ('NUBANK', 'NUBANK'), ('PAG_SEGURO', 'PAG SEGURO'), ('PAY_PAL', 'PAY PAL'), ('PIC_PAY', 'PIC PAY'), ('SANTANDER', 'SANTANDER'), ('OTHER', 'OUTRO')], max_length=30, null=True, verbose_name='Banco'),
        ),
    ]
