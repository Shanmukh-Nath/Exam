# Generated by Django 3.2 on 2022-11-08 06:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0022_auto_20221026_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam_model',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 8, 12, 3, 45, 184913)),
        ),
        migrations.AlterField(
            model_name='exam_model',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 8, 12, 3, 45, 184913)),
        ),
    ]
