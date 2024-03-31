import os, json
import pandas as pd
from django.db import models
from django.conf import settings
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import resolve
from .models import DebtorExcelBase, ClaimerExcelBase, FieldPreset
from .forms import ColumnMappingForm
from urllib.parse import unquote


def get_preset_names(request):
    # Fetch preset data from the database
    preset_data = FieldPreset.objects.all().values('name', 'preset_data')

    # Convert the queryset to a list of dictionaries
    preset_dicts = list(preset_data)

    # Return preset data as JSON response
    return JsonResponse(preset_dicts, safe=False)

def display_data(request):
    uploads_directory = os.path.join(settings.MEDIA_ROOT)
    files = list_files(uploads_directory)
    return render(request, 'file_list.html', {'files': files})

def select_directory(request, directory):
    uploads_directory = os.path.join(settings.MEDIA_ROOT, directory)
    files = list_files(uploads_directory)
    return render(request, 'select_directory.html', {'directory': directory, 'files': files})

def list_files(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.relpath(os.path.join(root, filename), settings.MEDIA_ROOT)
            files.append(file_path)
    return files



def save_selected_data(request, filename):
    resolved_filename = resolve(request.path_info).kwargs.get('filename')
    decoded_filename = unquote(resolved_filename)
    file_path = os.path.join(settings.MEDIA_ROOT, decoded_filename)

    try:
        df = pd.read_excel(file_path)
        subdirectory = os.path.dirname(decoded_filename)

        if subdirectory == 'debtor':
            Model = DebtorExcelBase
        elif subdirectory == 'claimer':
            Model = ClaimerExcelBase
        else:
            return render(request, 'file_not_found.html', {'error': f'Subdirectory "{subdirectory}" not recognized'}, status=404)

        excel_columns = list(df.columns)
        model_fields = {field.name: field.verbose_name for field in Model._meta.get_fields()}

        # Query FieldPreset model and retrieve the presets
        model_field_presets = {}
        field_presets = FieldPreset.objects.all()
        for preset in field_presets:
            model_field_presets[preset.name] = preset.preset_data

        if request.method == 'POST':
            form = ColumnMappingForm(request.POST, excel_columns=excel_columns, model_fields=model_fields)
            if form.is_valid():
                preset_choice = form.cleaned_data['preset_choice']
                if preset_choice:
                    preset_data = model_field_presets.get(preset_choice, {})
                    return JsonResponse(preset_data)
        else:
            form = ColumnMappingForm(excel_columns=excel_columns, model_fields=model_fields)

        return render(request, 'save_data_form.html', {'form': form})

    except FileNotFoundError:
        return render(request, 'file_not_found.html', {'error': f'File "{decoded_filename}" not found'}, status=404)







