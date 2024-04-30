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

def get_preset_data(request):
    if request.method == 'POST' and 'preset_name' in request.POST:
        preset_name = request.POST['preset_name']
        try:
            # Retrieve the preset object from the database
            preset = FieldPreset.objects.get(name=preset_name)
            # Return the preset data as JSON response
            return JsonResponse(preset.preset_data, safe=False)
        except FieldPreset.DoesNotExist:
            return JsonResponse({'error': 'Preset not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
def get_preset_names(request):
    if request.method == 'GET':
        presets = FieldPreset.objects.all().values_list('name', flat=True)
        return JsonResponse(list(presets), safe=False)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)    

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

        data_to_save = {}
        if request.method == 'POST':
            form = ColumnMappingForm(request.POST, excel_columns=excel_columns, model_fields=model_fields)
            if form.is_valid():
                preset_choice = form.cleaned_data.get('preset_choice')
                if preset_choice:
                    preset_data = model_field_presets.get(preset_choice, {})
                    for excel_column, field_name in preset_data.items():
                        data_to_save[field_name] = df[excel_column]
                else:
                    # If no preset is chosen, use the provided column-to-field mapping directly
                    column_to_field_mapping = form.cleaned_data
                    for excel_column, field_name in column_to_field_mapping.items():
                        data_to_save[field_name] = df[excel_column]

                # Save data_to_save to the respective model
                objects_to_create = []
                for i in range(len(data_to_save[list(data_to_save.keys())[0]])):
                    kwargs = {}
                    for field, data in data_to_save.items():
                        if field in ['admit_date', 'left_date']:
                            try:
                                kwargs[field] = datetime.strptime(data[i], '%d/%m/%Y').strftime('%Y-%m-%d')
                            except ValueError:
                                return JsonResponse({'error': f'Invalid date format in column "{field}"'}, status=400)
                        else:
                            kwargs[field] = data[i]
                    objects_to_create.append(Model(**kwargs))
                
                Model.objects.bulk_create(objects_to_create)

                return JsonResponse({'success': True})
        else:
            form = ColumnMappingForm(excel_columns=excel_columns, model_fields=model_fields)

        return render(request, 'save_data_form.html', {'form': form})

    except FileNotFoundError:
        return render(request, 'file_not_found.html', {'error': f'File "{decoded_filename}" not found'}, status=404)




