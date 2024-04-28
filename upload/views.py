from django.shortcuts import render
from .forms import FileUploadForm
from django import forms
import os
from pathlib import Path
from django.http import HttpResponse


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            location = form.cleaned_data['location']
            
            # Save the file to the selected location
            if location == 'debtor':
                save_location = 'uploads/debtor'
            elif location == 'claimer':
                save_location = 'uploads/claimer'
            else:
                save_location = 'uploads'
            
            file_path = os.path.join(save_location, uploaded_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            return render(request, 'success.html', {'message': 'File uploaded successfully.'})
    else:
        form = FileUploadForm()
    
    return render(request, 'upload.html', {'form': form})

def history_view(request):
    return render(request, "history.html")

def match_view(request):
    return render(request, "match.html")

def dashboard_view(request):
    return render(request, "dashboard.html")

<<<<<<< HEAD
def login_view(request):
    return render(request, 'login.html')    
=======
def result_view(request):
    return render(request,"result.html")

>>>>>>> origin/matchcolumns

