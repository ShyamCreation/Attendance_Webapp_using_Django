'''
Work time : 01 Jan 2024 to 15 May 2024
Made by Yadav Shyam (21SE02ML059),
           Anurag Panday (21SE02ML035).
contact: yadavshyam7048@gmail.com
Work in progress. here print statement is only for debug purpose. some of lines of code is not used in project.
'''
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Lecture)
admin.site.register(Lecturer)
admin.site.register(Attendance)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Timetable)
admin.site.register(Semester)
admin.site.register(TimeSlot)
admin.site.register(Enrollment)
admin.site.register(LectureRecord)