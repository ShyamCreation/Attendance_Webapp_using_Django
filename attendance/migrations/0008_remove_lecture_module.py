# Generated by Django 5.0.2 on 2024-02-27 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0007_remove_lecture_end_time_remove_lecture_start_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecture',
            name='module',
        ),
    ]
