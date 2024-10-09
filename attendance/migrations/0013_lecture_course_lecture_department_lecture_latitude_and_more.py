# Generated by Django 5.0.2 on 2024-02-27 17:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0012_course_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance.course'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance.department'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='latitude',
            field=models.DecimalField(decimal_places=6, default=1, max_digits=9),
        ),
        migrations.AddField(
            model_name='lecture',
            name='location',
            field=models.CharField(default=1, max_length=255),
        ),
        migrations.AddField(
            model_name='lecture',
            name='longitude',
            field=models.DecimalField(decimal_places=6, default=1, max_digits=9),
        ),
        migrations.AddField(
            model_name='lecture',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='semester',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance.semester'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='time_slot',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance.timeslot'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='lecturer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance.lecturer'),
        ),
    ]