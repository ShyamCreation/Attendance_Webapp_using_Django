# Generated by Django 5.0.2 on 2024-02-28 16:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0017_department_lecturer'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturer',
            name='latitude',
            field=models.FloatField(default=1),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='location',
            field=models.CharField(default=1, max_length=255),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='longitude',
            field=models.FloatField(default=1),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='time_slot',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance.timeslot'),
        ),
    ]
