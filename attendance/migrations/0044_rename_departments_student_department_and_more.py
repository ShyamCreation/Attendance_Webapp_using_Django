# Generated by Django 5.0.2 on 2024-03-07 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0043_lecturerecord'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='departments',
            new_name='department',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='semesters',
            new_name='semester',
        ),
    ]
