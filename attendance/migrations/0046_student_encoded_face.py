# Generated by Django 5.0.2 on 2024-03-09 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0045_lecturecount'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='encoded_face',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
