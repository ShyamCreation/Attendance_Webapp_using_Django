# Generated by Django 5.0.2 on 2024-02-27 18:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0016_alter_attendance_lecture'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='lecturer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance.lecturer'),
        ),
    ]