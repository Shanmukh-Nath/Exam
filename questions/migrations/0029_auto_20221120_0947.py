# Generated by Django 3.2 on 2022-11-20 04:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0028_auto_20221119_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam_model',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 20, 9, 47, 31, 362530)),
        ),
        migrations.AlterField(
            model_name='exam_model',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 20, 9, 47, 31, 362530)),
        ),
    ]
