# Generated by Django 3.2.7 on 2022-03-17 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accruals', '0004_auto_20210928_1220'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=3)),
                ('iso_code', models.IntegerField()),
                ('iso_title', models.CharField(max_length=3)),
            ],
        ),
        migrations.AddField(
            model_name='accrual',
            name='amount_USD',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='amount_USD',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accrual',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accruals', to='accruals.currency'),
        ),
        migrations.AddField(
            model_name='payment',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='accruals.currency'),
        ),
    ]