# Generated by Django 5.0.2 on 2024-02-27 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0010_timeslot_remove_attendance_lecture_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='Semester',
        ),
    ]
