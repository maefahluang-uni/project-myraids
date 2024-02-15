from django.shortcuts import render
from .forms import DataSelectionForm
from .models import ExcelBase
import pandas as pd
import os
from django.conf import settings

def parse_excel(filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{filename}' does not exist.")
    df = pd.read_excel(file_path)
    return df

def display_data(request):
    filename = 'example.xlsx'  # Change this to the actual filename
    try:
        df = parse_excel(filename)
        data = df.values.tolist()
        columns = df.columns.tolist()
        return render(request, 'display_data.html', {'data': data, 'columns': columns})
    except FileNotFoundError as e:
        return render(request, 'file_not_found.html', {'error': str(e)}, status=404)

def save_selected_data(request):
    if request.method == 'POST':
        form = DataSelectionForm(request.POST)
        if form.is_valid():
            selected_data = form.cleaned_data['selected_data']
            # Assuming selected_data contains the primary keys of ExcelBase objects
            # Fetch the selected objects and save them into the database or do whatever processing you need
            selected_objects = ExcelBase.objects.filter(pk__in=selected_data)
            for obj in selected_objects:
                # Save or process the selected objects here
                pass
            return render(request, 'success.html')
    else:
        form = DataSelectionForm()
    return render(request, 'data_selection.html', {'form': form})
