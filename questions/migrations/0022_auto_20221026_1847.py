# Generated by Django 3.2 on 2022-10-26 13:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0021_auto_20210408_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam_model',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 26, 18, 47, 36, 604110)),
        ),
        migrations.AlterField(
            model_name='exam_model',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 26, 18, 47, 36, 604110)),
        ),
    ]
