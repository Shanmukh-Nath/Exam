from django import forms
from .models import StudentInfo
from django.contrib.auth.models import User

class StudentForm(forms.ModelForm):
    
    class Meta():
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs = {'id':'passwordfield','class':'form-control'}),
            'email' : forms.EmailInput(attrs = {'id':'emailfield','class':'form-control'}),
            'username' : forms.TextInput(attrs = {'id':'usernamefield','class':'form-control'})
        }

class StudentInfoForm(forms.ModelForm):
    class Meta():
        model = StudentInfo
        fields = ['stream']
        widgets = {
            'stream' : forms.TextInput(attrs = {'class':'form-control'})
        }