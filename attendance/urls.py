'''
Made by Yadav Shyam (21SE02ML059),
           Anurag Panday (21SE02ML035).
Work time : 01 Jan 2024 to 15 May 2024
Work in progress. here print statement is only for debug purpose. some of lines of code is not used in project.
'''
from django.urls import path
from . import views

urlpatterns = [
    path('lecturer/register/', views.lecturer_register, name='lecturer_register'),
    path('student/register/', views.student_register, name='student_register'),
    path('accounts/login/', views.user_login, name='login'),
    path('', views.user_login, name='login'),
    path('lecturer/dashboard/', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('generate-qr-code/', views.generate_qr_code, name='generate_qr_code'),
    path('student/scan-qr-code/', views.scan_qr_code, name='scan_qr_code'),
    path('logout/', views.logout_view, name='logout'), 
    path('get-attendance-history/', views.get_attendance_history, name='get_attendance_history'),
    #path('upload-qr-code/', views.upload_qr_code, name='upload_qr_code'),
    path('face-recognition/', views.get_saved_face_data, name='face_recognition'),
    path('save-face-data/', views.save_face_data_view, name='save_face_data'),
    path('get-saved-face-data/', views.get_saved_face_data, name='get_saved_face_data'),
    path('face-data-list/', views.face_data_list, name='face_data_list'),
    path('filter/', views.filter_form, name='filter_form'),
    path('student-list/', views.student_list, name='student_list'),
    path('filter-and-list/', views.filter_and_list_students, name='filter_and_list_students'),
    #path('access-personal-details/', views.access_personal_details, name='access_personal_details'),
]

from django.conf import settings
from django.conf.urls.static import static

# Add this at the end of your urlpatterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
