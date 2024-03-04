import os
import pandas as pd
from django.db import models
from django.conf import settings
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import resolve
from .models import DebtorExcelBase, ClaimerExcelBase
from .forms import ColumnMappingForm
from urllib.parse import unquote


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
        

        if request.method == 'POST':
            form = ColumnMappingForm(request.POST, excel_columns=excel_columns, model_fields=model_fields)
            if form.is_valid():
                column_mapping = form.cleaned_data
                df = df.rename(columns=column_mapping)

                data = df.to_dict(orient='records')

                instances = [Model(**entry) for entry in data]

                # Convert date format from "DD/MM/YYYY" to "YYYY-MM-DD"
                for instance in instances:
                    instance.admit_date = datetime.strptime(instance.admit_date, "%d/%m/%Y").strftime("%Y-%m-%d") if instance.admit_date else None
                    instance.left_date = datetime.strptime(instance.left_date, "%d/%m/%Y").strftime("%Y-%m-%d") if instance.left_date else None

                Model.objects.bulk_create(instances)

                return HttpResponseRedirect(request.path_info)
        else:
            form = ColumnMappingForm(excel_columns=excel_columns, model_fields=model_fields)

        return render(request, 'save_data_form.html', {'form': form})

    except FileNotFoundError:
        return render(request, 'file_not_found.html', {'error': f'File "{decoded_filename}" not found'}, status=404)







