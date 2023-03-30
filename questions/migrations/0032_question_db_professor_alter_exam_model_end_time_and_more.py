# Generated by Django 4.1.7 on 2023-03-30 05:56

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0031_remove_question_db_professor_remove_question_db_tag_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question_db',
            name='professor',
            field=models.ForeignKey(limit_choices_to={'groups__name': 'Professor'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='exam_model',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 30, 11, 26, 52, 3085)),
        ),
        migrations.AlterField(
            model_name='exam_model',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 30, 11, 26, 52, 3085)),
        ),
        migrations.AlterField(
            model_name='question_db',
            name='question',
            field=models.CharField(max_length=1000000000000000000000000000000000000000000000000000000000000000000000000000000000),
        ),
    ]
