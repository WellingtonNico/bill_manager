# Generated by Django 4.1.1 on 2022-10-07 18:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BillRelatory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_year', models.IntegerField(verbose_name='Ano inicial')),
                ('end_year', models.IntegerField(verbose_name='Ano final')),
                ('start_month', models.IntegerField(choices=[(1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'), (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'), (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')], verbose_name='Mês inicial')),
                ('end_month', models.IntegerField(choices=[(1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'), (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'), (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')], verbose_name='Mês final')),
                ('created_date', models.DateTimeField()),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('data', models.JSONField(blank=True, default=dict, null=True)),
                ('status', models.CharField(choices=[('NEW', 'Novo'), ('CREATED', 'Criado'), ('QUEUED', 'Na fila'), ('PENDING', 'Pendente'), ('PROCESSING', 'Processando'), ('COMPLETED', 'Completo'), ('ERROR', 'Erro')], default='NEW', max_length=12, verbose_name='Status')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Relatório de Contas',
                'verbose_name_plural': 'Relatórios de Contas',
            },
        ),
    ]
