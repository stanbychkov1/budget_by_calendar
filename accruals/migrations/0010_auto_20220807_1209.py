# Generated by Django 3.2.7 on 2022-08-07 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accruals', '0009_currency_priority'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accrual',
            options={'ordering': ('date',), 'verbose_name': 'Начисление', 'verbose_name_plural': 'Начисления'},
        ),
        migrations.AlterModelOptions(
            name='currency',
            options={'verbose_name': 'Валюта', 'verbose_name_plural': 'Валюты'},
        ),
        migrations.AlterModelOptions(
            name='method',
            options={'verbose_name': 'Метод', 'verbose_name_plural': 'Методы'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ('date',), 'verbose_name': 'Оплата', 'verbose_name_plural': 'Оплаты'},
        ),
        migrations.AlterModelOptions(
            name='rate',
            options={'get_latest_by': ('-date',), 'verbose_name': 'Курс', 'verbose_name_plural': 'Курсы'},
        ),
    ]
