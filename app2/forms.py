from django import forms
# from django.conf import User
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UploadedFile 


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
