# Generated by Django 4.1.1 on 2022-10-03 00:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bill_chargers', '0001_initial'),
        ('bill_categories', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_type', models.CharField(choices=[('FIXED', 'FIXA'), ('INSTALLED', 'PARCELADA'), ('UNIQUE_INSTALLMENT', 'PARCELA ÚNICA')], max_length=18, verbose_name='Tipo')),
                ('installment_number', models.IntegerField(blank=True, null=True, verbose_name='Número da parcela')),
                ('create_date', models.DateField(verbose_name='Data de criação')),
                ('expiration_date', models.DateField(blank=True, null=True, verbose_name='Data de vencimento')),
                ('expiration_notification_date', models.DateField(blank=True, null=True, verbose_name='Data para notificar vencimento')),
                ('status', models.CharField(choices=[('UNDEFINED', 'INDEFINIDO'), ('TO_EXPIRE', 'A VENCER'), ('EXPIRED', 'EXPIRADA'), ('WARNING', 'ATENÇÃO')], default='UNDEFINED', max_length=9)),
                ('bill_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill_categories.billcategory', verbose_name='Categoria')),
                ('bill_charger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill_chargers.billcharger', verbose_name='Cobrador')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
        ),
    ]