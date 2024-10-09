'''
Made by Yadav Shyam (21SE02ML059),
           Anurag Panday (21SE02ML035).
contact: yadavshyam7048@gmail.com
Work time : 01 Jan 2024 to 15 May 2024
Work in progress. here print statement is only for debug purpose. some of lines of code is not used in project.
'''
from django import forms
from .models import *

class LecturerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email address already exists.")
        return email
        

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    #date_of_birth = forms.DateField(label='Date of Birth: YYYY-MM-DD', required=True)
    profile_picture = forms.ImageField(label='Profile Picture', required=True)
    #face_image = forms.ImageField(label='Face Image')


    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'profile_picture')
        widgets = {
            'username': forms.TextInput(attrs={'required': True}),
            'first_name': forms.TextInput(attrs={'required': True}),
            'last_name': forms.TextInput(attrs={'required': True}),
            'email': forms.EmailInput(attrs={'required': True}),
        }
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email address already exists.")
        return email

class LoginForm(forms.Form):
    username = forms.CharField(label='Enrollment_Id / Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
