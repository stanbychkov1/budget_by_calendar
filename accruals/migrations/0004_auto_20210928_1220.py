# Generated by Django 3.2.7 on 2021-09-28 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accruals', '0003_alter_patient_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accrual',
            name='payment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accruals', to='accruals.payment'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='payments', to='accruals.method'),
        ),
    ]
