'''
Made by Yadav Shyam (21SE02ML059),
           Anurag Panday (21SE02ML035).
contact: yadavshyam7048@gmail.com
Work time : 01 Jan 2024 to 15 May 2024
Work in progress. here print statement is only for debug purpose. some of lines of code is not used in project.
'''
from django.db import models
from .models import *
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils import timezone
#import face_recognition

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Semester(models.Model):
    name = models.CharField(max_length=100)  # Add a field for the semester's name

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True )
    last_name = models.CharField(max_length=100, blank=True, null=True )
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    # Add other fields like name, roll number, etc.
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True, blank=True)
    encoded_face = models.BinaryField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    face_data = models.TextField(blank=True, null=True)

    def save_face_data(self, image_data):
        # Save the base64-encoded image data to the face_data field
        #print("Image data:", image_data)
        self.face_data = image_data
        self.save()
    

    '''def save_encoded_face(self, image_path):
        # Load the image and encode the face
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        
        if face_encodings:
            # Convert the face encodings to a compatible data type
            encoded_face_bytes = face_encodings[0].tobytes()
            
            # Store the encoded face in the database
            self.encoded_face = encoded_face_bytes
            self.save()
            return True
        else:
            return False'''
        
    def __str__(self):
        return f"{self.user.username} - {self.department} - {self.semester}"
    
class Course(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

from django.db import models

class TimeSlot(models.Model):
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

class Lecturer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True )
    last_name = models.CharField(max_length=100, blank=True, null=True )
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    departments = models.ManyToManyField(Department)
    courses = models.ManyToManyField(Course)
    semesters = models.ManyToManyField(Semester)
    time_slot = models.ManyToManyField(TimeSlot)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    # Add other fields like name, email, etc.
    
    def __str__(self):
        return self.user.username


class Lecture(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, default=1)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, default=1)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, default=1)
    location = models.CharField(max_length=255, default=1)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, default=1)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, default=1)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    qr_code_id = models.CharField(max_length=32, unique=True, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.time_slot} - {self.department} - {self.course} - {self.semester}"

class Attendance(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendance_status = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    qr_code_id = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.lecture.course}"

class Timetable(models.Model):
    lecturer = models.ForeignKey('Lecturer', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=20, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ])
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.day_of_week} - {self.time_slot} - {self.department} - {self.course} - {self.semester}"
    
from django.db import models

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} - {self.department} - {self.semester}"

class LectureRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    num_lectures_attended = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.user.username} - {self.department} - {self.semester}"

class LectureCount(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    lecture_count = models.IntegerField(default=0)