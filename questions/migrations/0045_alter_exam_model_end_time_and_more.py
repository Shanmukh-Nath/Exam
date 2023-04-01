# Generated by Django 4.1.7 on 2023-04-01 01:56

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0044_randomquestion_choice_alter_exam_model_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam_model',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 1, 7, 26, 46, 814450)),
        ),
        migrations.AlterField(
            model_name='exam_model',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 1, 7, 26, 46, 814450)),
        ),
        migrations.AlterField(
            model_name='question_db',
            name='professor',
            field=models.ForeignKey(default=22, limit_choices_to={'groups__name': 'Professor'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
