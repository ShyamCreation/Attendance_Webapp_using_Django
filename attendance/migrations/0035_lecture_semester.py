# Generated by Django 5.0.2 on 2024-02-29 07:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0034_lecturer_semesters'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='semester',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance.semester'),
        ),
    ]
