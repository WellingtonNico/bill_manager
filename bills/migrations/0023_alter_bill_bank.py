# Generated by Django 4.1.1 on 2022-10-07 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0022_alter_bill_payment_type_alter_bill_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='bank',
            field=models.CharField(blank=True, choices=[('BANCO_DO_BRASIL', 'Banco do Brasil'), ('BRADESCO', 'Bradesco'), ('CAIXA', 'Caixa'), ('ITAU', 'Itaú'), ('ITI', 'Iti'), ('MERCADO_PAGO', 'Mercado Pago'), ('NUBANK', 'Nubank'), ('PAG_SEGURO', 'Pag Seguro'), ('PAY_PAL', 'Pay Pal'), ('PIC_PAY', 'Pic Pay'), ('SANTANDER', 'Santander'), ('BANCO_CORA', 'Banco Cora'), ('OTHER', 'Outro')], max_length=30, null=True, verbose_name='Banco'),
        ),
    ]