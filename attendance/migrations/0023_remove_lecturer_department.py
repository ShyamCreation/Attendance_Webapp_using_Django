# Generated by Django 5.0.2 on 2024-02-28 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0022_lecturer_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecturer',
            name='department',
        ),
    ]
