# Generated by Django 4.1.7 on 2023-03-30 05:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0036_alter_exam_model_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam_model',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 30, 11, 29, 12, 572937)),
        ),
        migrations.AlterField(
            model_name='exam_model',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 30, 11, 29, 12, 572937)),
        ),
        migrations.AlterField(
            model_name='question_db',
            name='question',
            field=models.CharField(max_length=100000000),
        ),
    ]
