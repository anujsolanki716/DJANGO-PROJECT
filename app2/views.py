from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegistrationForm, FileUploadForm
from .models import UploadedFile
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
import os

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('upload_file')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('upload_file')
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            file.save()
    else:
        form = FileUploadForm()
    files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'upload.html', {'form': form, 'files': files})



@login_required
def view_file(request):
    files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'view_file.html', {'files': files})

@login_required
def download_file(request, file_id):
    file_obj = UploadedFile.objects.get(id=file_id)
    file_path = file_obj.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = FileResponse(file)
            response['Content-Disposition'] = f'attachment; filename="{file_obj.file.name}"'
            return response
    return render(request, 'file_not_found.html')

