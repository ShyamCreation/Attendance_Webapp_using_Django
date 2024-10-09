'''
Made by Yadav Shyam (21SE02ML059),
           Anurag Panday (21SE02ML035).
Work time : 01 Jan 2024 to 15 May 2024
Work in progress. here print statement is only for debug purpose. some of lines of code is not used in project.
'''
from django.shortcuts import render

#Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import LecturerRegistrationForm, StudentRegistrationForm, LoginForm

#this is for  registration of lectuter/faculty
def lecturer_register(request):
    if request.method == 'POST':
        form = LecturerRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = CustomUser.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password, is_lecturer=True)
            Lecturer.objects.create(user=user, first_name=first_name, last_name=last_name, email=email)
            return redirect('login')
    else:
        form = LecturerRegistrationForm()
    return render(request, 'lecturer_register.html', {'form': form})

def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            #face_image = request.FILES['face_image']
            profile_picture = form.cleaned_data['profile_picture']
            # Create a new CustomUser instance
            user = CustomUser.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password, is_student=True)
            
            # Create a new Student instance associated with the user
            student = Student.objects.create(user=user, first_name=first_name, last_name=last_name, email=email)
            if profile_picture:  # Check if a picture was uploaded
                student.profile_picture = profile_picture
                student.save()
            # Save the encoded face data
            #student.save_encoded_face(face_image)
            
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'student_register.html', {'form': form})



from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_lecturer:
                    return redirect('lecturer_dashboard')
                elif user.is_student:
                    return redirect('student_dashboard')
            else:
                messages.error(request, 'Username or password is incorrect.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


from django.shortcuts import render
from .models import Lecture, Attendance

@login_required
def lecturer_dashboard(request):
    lecturer = request.user.lecturer
    lectures = Lecture.objects.filter(lecturer=lecturer)
    qr_codes = Lecture.objects.filter(lecturer=lecturer).order_by('-id')[:7]
    attendance_history = Attendance.objects.filter(lecture__in=lectures)
    timetable = Timetable.objects.filter(lecturer=lecturer)
    time_slots = TimeSlot.objects.all()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    context = {
        'user': request.user,
        'qr_codes': qr_codes,
        'attendance_history': attendance_history,
        'timetable': timetable,
        'time_slots': time_slots,
        'days': days,
    }
    return render(request, 'lecturer_dashboard.html', context)


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Lecture, Attendance
from django.utils import timezone
from .models import Student

@login_required
def student_dashboard(request):
    # Retrieve the logged-in student
    student = request.user.student
    # Retrieve the department and semester of the student from the related Student model
    department = student.department
    semester = student.semester
    
    # Fetch attendance records for the student based on department and semester
    attendance_records = Attendance.objects.filter(student=student, lecture__department=department, lecture__semester=semester)
    lectures_conducted = Lecture.objects.filter(
        department=department, semester=semester
    ).order_by('-id')[:7]

    lectures_attended = Attendance.objects.filter(student=student, lecture__department=department, lecture__semester=semester).order_by('-id')[:7]
    # Fetch total number of lectures conducted for the specific department and semester
    total_lectures_conducted = Lecture.objects.filter(department=department, semester=semester).count()
    
    # Calculate the total number of lectures attended by the student
    total_attended_lectures = attendance_records.count()
    
    # Calculate attendance percentage
    if total_lectures_conducted > 0:
        attendance_percentage = (total_attended_lectures / total_lectures_conducted) * 100
    else:
        attendance_percentage = 0
    attendance_percentage = format(attendance_percentage, '.2f')

    # Render the student dashboard with attendance information
    context = {
        'department': department,
        'semester': semester,
        'total_attended_lectures': total_attended_lectures,
        'total_lectures_conducted': total_lectures_conducted,
        'attendance_percentage': attendance_percentage,
        'lectures_conducted': lectures_conducted,
        'lectures_attended': lectures_attended
        # Add any other context data you need for the student dashboard
    }
    return render(request, 'student_dashboard.html', context)


#generate new qr code of lecture 
import qrcode
import uuid
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Lecture, Timetable, Department, Course, Semester
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from datetime import datetime, timedelta

@login_required
def generate_qr_code(request):
    lecturer = request.user.lecturer

    if request.method == 'POST':
        time_slot_id = request.POST.get('time_slot') #Required detail about lecture
        department_id = request.POST.get('department')
        course_id = request.POST.get('course')
        semester_id = request.POST.get('semester')
        location = request.POST.get('location')
        longitude = request.POST.get('longitude')
        latitude = request.POST.get('latitude')

        time_slot = TimeSlot.objects.get(id=time_slot_id)
        department = Department.objects.get(id=department_id)
        course = Course.objects.get(id=course_id)
        semester = Semester.objects.get(id=semester_id)

        # Get expiration time from the form input
        expiration_time = datetime.now() + timedelta(minutes=1)
        expiration_time_str = expiration_time.strftime('%Y-%m-%d %H:%M:%S')

        # Check if expiration time is in the future
        if expiration_time > datetime.now():
            # Generate a unique QR code ID
            qr_code_id = uuid.uuid4().hex #formate of qrcode store in db

            # Create QR code data including expiration time and QR code ID
            qr_data = f"Lecturer: {request.user.username}, QR Code ID: {qr_code_id}, Time Slot: {time_slot}, Department: {department}, Course: {course}, Semester: {semester}, Latitude: {latitude}, Longitude: {longitude}, Expiration Time: {expiration_time_str}"

            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=6,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            # Create an image from the QR code
            img = qr.make_image(fill_color="black", back_color="white")

            # Save the image to a BytesIO buffer
            buffer = BytesIO()
            img.save(buffer, format='PNG')

            # Create a file from the buffer
            image_file = ContentFile(buffer.getvalue())

            # Save image path and QR code ID to Lecture model
            lecture = Lecture.objects.create(
                lecturer=lecturer,
                time_slot=time_slot,
                department=department,
                course=course,
                semester=semester,
                location=location,
                longitude=longitude,
                latitude=latitude,
                qr_code_id=qr_code_id,
            )
            lecture.qr_code.save(f'lecture_{qr_code_id}.png', image_file)
            img_path = lecture.qr_code.url

            return render(request, 'qr_code_generated.html', {'img_path': img_path})
        else:
            # Return error if expiration time is not in the future
            return render(request, 'qr_code_date_error.html', {'error_message': 'Expiration time must be in the future.'})

    else: #to get choices about lecture
        time_slot_choices = [(time_slot.id, str(time_slot)) for time_slot in lecturer.time_slot.all()]
        department_choices = [(department.id, department.name) for department in lecturer.departments.all()]
        course_choices = [(course.id, course.name) for course in lecturer.courses.all()]
        semester_choices = [(semester.id, semester.name) for semester in lecturer.semesters.all()]

        return render(request, 'generate_qr_code.html', {
            'time_slot_choices': time_slot_choices,
            'department_choices': department_choices,
            'course_choices': course_choices,
            'semester_choices': semester_choices,
        })




from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render
from .models import Attendance

def get_attendance_history(request):
    # Fetch attendance history for the logged-in student
    attendance_history = Attendance.objects.filter(student=request.user.student)
    
    context = {
        'attendance_history': attendance_history,
    }
    
    return render(request, 'attendance_history.html', context)

import io
from django.http import JsonResponse
from PIL import Image
import base64
from io import BytesIO
from pyzbar.pyzbar import decode
'''
def upload_qr_code(request): #this is for test purpose
    if request.method == 'POST':
        # Get the uploaded QR code image from the request
        qr_code_image = request.FILES.get('qr_code_image')

        if qr_code_image:
            # Read the image data from the uploaded file
            image_data = qr_code_image.read()
            print("Image data size:", len(image_data))
            # Decode the image data
            decoded_qr_code_data = decode_qr_code(image_data)

            if decoded_qr_code_data:
                # Extract the QR code data
                qr_code_data = decoded_qr_code_data[0].data.decode('utf-8')
                print("Decoded data:", qr_code_data)
                # Return the QR code data in the response
                return JsonResponse({'qr_code_data': qr_code_data})
            else:
                print("No QR code found in the image")
                return JsonResponse({'error_message': 'No QR code found in the uploaded image'}, status=400)
        else:
            print("No QR code image uploaded")
            return JsonResponse({'error_message': 'No QR code image uploaded'}, status=400)
    else:
        return JsonResponse({'error_message': 'Invalid request method'}, status=405)
'''
def decode_qr_code(image_data):
    try:
        # Open the image using PIL (Python Imaging Library)
        image = Image.open(BytesIO(image_data))
        print("Image opened successfully")
        # Decode the QR code image
        qr_codes = decode(image)

        return qr_codes
    except Exception as e:
        print(f'Error decoding QR code image: {str(e)}')
        return None

@login_required
def scan_qr_code(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        qr_code_data = request.POST.get('qr_code_data')

        print("Latitude:", latitude)
        print("Longitude:", longitude)
        print("QR Code Data:")

        try:
            image_data = base64.b64decode(qr_code_data.split(",")[1])
            image = Image.open(io.BytesIO(image_data))
            qr_codes = decode(image)
        except Exception as e:
            print(f'Error decoding QR code image: {str(e)}')
            return render(request, 'qr_code_error.html', {'error_message': f'Error decoding QR code image: {str(e)}'}, status=400)

        if qr_codes:
            qr_data = qr_codes[0].data.decode('utf-8').split(', ')
            #print("QR Data:", qr_data)

            try:
                lecturer_username = qr_data[0].split(': ')[1]
                lecture_department = qr_data[3].split(': ')[1]
                lecture_semester = qr_data[5].split(': ')[1]
                qr_code_id = qr_data[1].split(': ')[1]
                expiration_time_str = qr_data[8].split(': ')[1]
                latitude_str = qr_data[6].split(': ')[1]
                longitude_str = qr_data[7].split(': ')[1]

                #print("Lecturer Username:", lecturer_username) #test purpose
                #print("Lecture Department:", lecture_department)
                #print("Lecture Semester:", lecture_semester)
                #print("QR Code ID:", qr_code_id)
                #print("Expiration Time:", expiration_time_str)
                #print("Latitude from QR:", latitude_str)
                #print("Longitude from QR:", longitude_str)

                latitude_float = float(latitude)
                longitude_float = float(longitude)

                threshold = 0.000089/5 # 5 Meters or radius allowed for student
                if (abs(latitude_float - float(latitude_str)) < threshold and
                    abs(longitude_float - float(longitude_str)) < threshold):

                    #print("Location within Threshold")

                    expiration_time = datetime.strptime(expiration_time_str, '%Y-%m-%d %H:%M:%S')
                    current_time = datetime.now()

                    if current_time >= expiration_time:
                        print("QR Code Not Expired")

                        lecture = Lecture.objects.filter(
                            lecturer__user__username=lecturer_username,
                            department__name=lecture_department,
                            semester__name=lecture_semester,
                            qr_code_id=qr_code_id
                        ).first()
                        #print("Lecture:", lecture)

                        if lecture:
                            # Check if the student belongs to the same department and semester
                            student_department = getattr(request.user.student, 'department', None)
                            student_semester = getattr(request.user.student, 'semester', None)

                            if request.user.is_student and student_department and student_department.name == lecture_department and student_semester and student_semester.name == lecture_semester:
                                #print("Student belongs to Department and Semester")
                                # Check if attendance already marked for this lecture and student
                                if not Attendance.objects.filter(lecture=lecture, student=request.user.student, qr_code_id=qr_code_id).exists():
                                    print("Attendance Not Marked Yet")
                                    # Mark attendance for the corresponding lecture
                                    Attendance.objects.create(lecture=lecture, student=request.user.student, attendance_status=True, qr_code_id=qr_code_id)
                                    return render(request, 'qr_code_success.html', {'success_message': 'Attendance marked successfully'}, status=200)
                                else:
                                    #print("Attendance Already Marked")
                                    return render(request, 'qr_code_error.html', {'error_message': 'Attendance already marked for this lecture'}, status=400)
                            else:
                                #print("Student does not belong to this Department or Semester")
                                return render(request, 'qr_code_error.html', {'error_message': 'Student does not belong to this department or semester'}, status=400)
                        else:
                            #print("No matching lecture found")
                            return render(request, 'qr_code_error.html', {'error_message': 'No matching lecture found'}, status=400)
                    else:
                        #print("QR code has expired")
                        return render(request, 'qr_code_error.html', {'error_message': 'QR code has expired'}, status=400)
                else:
                   # print("Student location does not match QR code location")
                    return render(request, 'qr_code_error.html', {'error_message': 'Student location does not match QR code location'}, status=400)
            except IndexError:
                #print("Error parsing QR code data")
                return render(request, 'qr_code_error.html', {'error_message': 'Error parsing QR code data'}, status=400)
        else:
            #print("No QR code detected")
            return render(request, 'qr_code_error.html', {'error_message': 'No QR code detected'}, status=400)
    else:
        return render(request, 'scan_qr_code.html')

# views.py in your Django app folder

from django.shortcuts import render

from django.http import JsonResponse
from .models import Student

def get_saved_face_data(request):
    student = request.user.student
    if request.method == 'GET':
        # Retrieve saved face data from the database
        saved_face_data = Student.objects.values('id', 'face_data')

        # Convert queryset to list of dictionaries
        face_data_list = list(saved_face_data)

        # Return the face data as JSON response
        return JsonResponse(face_data_list, safe=False)

# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import Student
@login_required
def save_face_data_view(request):
    student = request.user.student
    if request.method == 'POST':
        captured_image_data = request.POST.get('image_data')
        print(len(captured_image_data))
        #print("Image data:", captured_image_data)
        # Assuming the user is logged in and you have access to the Student object
        student = request.user.student
        student.save_face_data(captured_image_data)
        
        # Return success response
        return render(request,'scan_qr_code.html')
    else:
        # Handle GET request
        return render(request, 'save_face_data.html')


# views.py
'''
# views.py
import numpy as np 
import face_recognition
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student

@login_required
def access_personal_details(request):
    if request.method == 'POST':
        uploaded_image = request.FILES['image']
        student = request.user.student
        
        if student.encoded_face:
            unknown_image = face_recognition.load_image_file(uploaded_image)
            unknown_face_encoding = face_recognition.face_encodings(unknown_image)
            
            if len(unknown_face_encoding) > 0:
                # Convert the encoded face from the database to a numpy array
                known_face_encoding = np.frombuffer(student.encoded_face, dtype=np.float64)
                
                # Perform the face comparison
                result = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding[0], tolerance=0.6)
                
                if result[0]:
                    return JsonResponse({'success_message': 'Matched successfully'}, status=200)  # Redirect to personal details page if face matches
                else:
                    messages.error(request, "Face doesn't match. Please try again.")
            else:
                messages.error(request, "No face detected in the uploaded image. Please try again.")
        else:
            messages.error(request, "Face data is not available for the current user.")

    return render(request, 'access_personal_details.html')

'''

# views.py

# views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # Import the login_required decorator
from .models import Student

@login_required  # Apply the login_required decorator to ensure the user is authenticated
def face_data_list(request):
    if hasattr(request.user, 'student'):  # Check if the authenticated user has a student profile
        student = request.user.student
        students = [student]  # Assuming you want to display the face data of the current user only
    else:
        students = []  # If the user is not authenticated or doesn't have a student profile, return an empty list

    return render(request, 'face_data_list.html', {'students': students})


from django.shortcuts import render
from .models import Student, Department, Semester

def filter_form(request):
    departments = Department.objects.all()
    semesters = Semester.objects.all()
    return render(request, 'filter_form.html', {'departments': departments, 'semesters': semesters})

def student_list(request):
    if request.method == 'POST':
        department_id = request.POST.get('department')
        print(department_id)
        semester_id = request.POST.get('semester')
        
        # Get the list of students based on department and semester
        students = Student.objects.filter(department_id=department_id, semester_id=semester_id)
        
        return render(request, 'student_list.html', {'students': students})
    
    return render(request, 'filter_form.html')

from django.shortcuts import render
from .models import Student, Department, Semester

def filter_and_list_students(request):
    lecturer = request.user.lecturer
    departments = lecturer.departments.all()
    semesters = lecturer.semesters.all()
    students = None

    if request.method == 'POST':
        department_id = request.POST.get('department')
        print("department_id", department_id)
        semester_id = request.POST.get('semester')
        
        # Filter students based on department and semester
        students = Student.objects.filter(department_id=department_id, semester_id=semester_id)

    return render(request, 'filter_and_list_students.html', {'departments': departments, 'semesters': semesters, 'students': students})
