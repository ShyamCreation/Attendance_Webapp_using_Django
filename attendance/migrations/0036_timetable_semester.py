# Generated by Django 5.0.2 on 2024-02-29 07:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0035_lecture_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='semester',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance.semester'),
        ),
    ]
