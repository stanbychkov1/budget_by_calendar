# Generated by Django 3.2.7 on 2022-03-29 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accruals', '0008_auto_20220323_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]
