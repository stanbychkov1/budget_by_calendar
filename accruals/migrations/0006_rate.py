# Generated by Django 3.2.7 on 2022-03-22 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accruals', '0005_auto_20220317_1735'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=10, max_digits=10)),
                ('nominal', models.IntegerField()),
                ('date', models.DateField(db_index=True)),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rate', to='accruals.currency')),
            ],
        ),
    ]
