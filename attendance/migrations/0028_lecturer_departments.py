# Generated by Django 5.0.2 on 2024-02-29 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0027_remove_lecturer_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturer',
            name='departments',
            field=models.ManyToManyField(related_name='lecturers', to='attendance.department'),
        ),
    ]
