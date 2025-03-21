# Generated by Django 5.0.2 on 2024-02-27 17:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0013_lecture_course_lecture_department_lecture_latitude_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=20)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.course')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.department')),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.lecturer')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.semester')),
                ('time_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.timeslot')),
            ],
        ),
    ]
