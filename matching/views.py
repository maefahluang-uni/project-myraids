import os
import pandas as pd
from django.conf import settings
from django.shortcuts import render
from .forms import DataSelectionForm
from .models import ExcelBase
from django.utils.http import unquote
from django.urls import resolve


def list_files(directory):
    files = []
    print("Directory:", directory)
    for root, _, filenames in os.walk(directory):
        print("Root:", root)
        for filename in filenames:
            file_path = os.path.relpath(os.path.join(root, filename), settings.MEDIA_ROOT)
            print("File path:", file_path)
            files.append(file_path)
    return files


def display_data(request):
    uploads_directory = os.path.join(settings.MEDIA_ROOT,)
    files = list_files(uploads_directory)
    return render(request, 'file_list.html', {'files': files})


def save_selected_data(request, filename):
    # Extract the filename from the URL pattern
    resolved_filename = resolve(request.path_info).kwargs.get('filename')
    
    # Decode the filename
    decoded_filename = unquote(resolved_filename)
    
    file_path = os.path.join(settings.MEDIA_ROOT, decoded_filename)
    
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        # Convert the data to a list of dictionaries
        data = df.to_dict(orient='records')
        # Pass the data to the template
        return render(request, 'display_data.html', {'data': data, 'filename': decoded_filename})
    except FileNotFoundError:
        return render(request, 'file_not_found.html', {'error': f'File "{decoded_filename}" not found'}, status=404)

def select_directory(request, directory):
    uploads_directory = os.path.join(settings.MEDIA_ROOT, directory)
    files = list_files(uploads_directory)
    return render(request, 'select_directory.html', {'directory': directory, 'files': files})
