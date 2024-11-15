# Generated by Django 5.0.2 on 2024-03-07 05:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0042_rename_department_student_departments_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LectureRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_lectures_attended', models.IntegerField(default=0)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.department')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.student')),
            ],
        ),
    ]
