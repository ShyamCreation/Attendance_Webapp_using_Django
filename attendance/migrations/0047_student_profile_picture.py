# Generated by Django 5.0.2 on 2024-03-26 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0046_student_encoded_face'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='profile_pics/'),
        ),
    ]