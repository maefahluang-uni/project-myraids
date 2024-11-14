# matching/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Comparison, ColumnSelection, ComparisonResult
from .forms import FileSelectionForm, ColumnSelectionForm, ColumnPairingForm
from .utils import load_columns_from_file, create_combined_column_names
import pandas as pd

@login_required
def home(request):
    """Home view for the matching app."""
    comparisons = Comparison.objects.filter(user=request.user)
    return render(request, 'matching/home.html', {'comparisons': comparisons})

@login_required
def load_columns(request):
    """AJAX view to load columns from the selected files and check for equal column count."""
    file1_id = request.GET.get('file1_id')
    file2_id = request.GET.get('file2_id')

    # Load columns from both files
    columns_file1, _ = load_columns_from_file(file1_id)
    columns_file2, _ = load_columns_from_file(file2_id)

    # Check if columns have equal count
    columns_equal = len(columns_file1) == len(columns_file2)

    return JsonResponse({
        'columns_file1': columns_file1,
        'columns_file2': columns_file2,
        'columns_equal': columns_equal,
        'message': "Please select an equal number of columns." if not columns_equal else ""
    })

@login_required
def create_comparison(request):
    """View to create a new comparison."""
    if request.method == 'POST':
        form = FileSelectionForm(request.POST)
        if form.is_valid():
            file1 = form.cleaned_data['excel_file_1']
            file2 = form.cleaned_data['excel_file_2']

            # Load columns from the selected files
            columns_file1, _ = load_columns_from_file(file1.id)
            columns_file2, _ = load_columns_from_file(file2.id)

            # Save selections and columns in the session
            request.session['file1_id'] = file1.id
            request.session['file2_id'] = file2.id
            request.session['columns_file1'] = columns_file1
            request.session['columns_file2'] = columns_file2

            return redirect('matching:column_selection')
    else:
        form = FileSelectionForm()

    return render(request, 'matching/create_comparison.html', {'form': form})

@login_required
def select_columns(request):
    """View to handle user column selection based on file columns."""
    columns_file1 = request.session.get('columns_file1', [])
    columns_file2 = request.session.get('columns_file2', [])

    if request.method == 'POST':
        form = ColumnSelectionForm(request.POST, file1_columns=columns_file1, file2_columns=columns_file2)
        if form.is_valid():
            selected_columns_file1 = form.cleaned_data['columns_file1']
            selected_columns_file2 = form.cleaned_data['columns_file2']
            common_column = form.cleaned_data['common_column']

            # Check if columns match; if not, redirect to manual pairing
            if set(selected_columns_file1) != set(selected_columns_file2):
                request.session['selected_columns_file1'] = selected_columns_file1
                request.session['selected_columns_file2'] = selected_columns_file2
                request.session['common_column'] = common_column
                return redirect('matching:pair_columns')

            # Columns match, proceed to create the Comparison instance
            comparison = Comparison.objects.create(
                user=request.user,
                file1_id=request.session['file1_id'],
                file2_id=request.session['file2_id'],
                common_column=common_column
            )

            # Save the column mappings directly if no manual pairing needed
            combined_columns = create_combined_column_names(selected_columns_file1, selected_columns_file2)
            for col1, col2, combined_name in zip(selected_columns_file1, selected_columns_file2, combined_columns):
                ColumnSelection.objects.create(
                    comparison=comparison,
                    column_file1=col1,
                    column_file2=col2,
                    combined_column_name=combined_name
                )

            return redirect('matching:compare_results', comparison_id=comparison.id)
    else:
        form = ColumnSelectionForm(file1_columns=columns_file1, file2_columns=columns_file2)

    return render(request, 'matching/select_columns.html', {'form': form})

@login_required
def pair_columns(request):
    """View for manually pairing columns between two files if there are mismatches."""
    selected_columns_file1 = request.session.get('selected_columns_file1', [])
    selected_columns_file2 = request.session.get('selected_columns_file2', [])

    if request.method == 'POST':
        form = ColumnPairingForm(request.POST, columns_file1=selected_columns_file1, columns_file2=selected_columns_file2)
        if form.is_valid():
            # Create Comparison instance
            comparison = Comparison.objects.create(
                user=request.user,
                file1_id=request.session['file1_id'],
                file2_id=request.session['file2_id'],
                common_column=request.session['common_column']
            )

            # Save column mappings based on user input
            for col1 in selected_columns_file1:
                col2 = form.cleaned_data[f'pair_{col1}']
                combined_name = f"{col1}_{col2}"
                ColumnSelection.objects.create(
                    comparison=comparison,
                    column_file1=col1,
                    column_file2=col2,
                    combined_column_name=combined_name
                )

            return redirect('matching:compare_results', comparison_id=comparison.id)
    else:
        form = ColumnPairingForm(columns_file1=selected_columns_file1, columns_file2=selected_columns_file2)

    return render(request, 'matching/pair_columns.html', {'form': form})

@login_required
def compare_results(request, comparison_id):
    """View to display the results of the comparison."""
    comparison = get_object_or_404(Comparison, id=comparison_id, user=request.user)
    column_selections = comparison.column_selections.all()

    # Load dataframes for comparison
    file1_id = comparison.file1.id
    file2_id = comparison.file2.id
    _, df1 = load_columns_from_file(file1_id)
    _, df2 = load_columns_from_file(file2_id)

    # Retrieve the selected instance names
    file1_name = str(comparison.file1)
    file2_name = str(comparison.file2)

    # Create combined column names for each pairing
    combined_columns = [
        f"{sel.column_file1}_{sel.column_file2}" for sel in column_selections
    ]

    # Perform comparison based on common column and mapped columns
    results = []
    for _, row1 in df1.iterrows():
        for _, row2 in df2.iterrows():
            if row1[comparison.common_column] == row2[comparison.common_column]:
                common_value = row1[comparison.common_column]

                # Data for file1 and file2 separately using combined column names
                data_file1 = {f"{sel.column_file1}_{sel.column_file2}": row1[sel.column_file1] for sel in column_selections}
                data_file2 = {f"{sel.column_file1}_{sel.column_file2}": row2[sel.column_file2] for sel in column_selections}
                status = 'Match' if data_file1 == data_file2 else 'Mismatch'
                description = 'All data matches' if status == 'Match' else 'Data differs'

                # Append separate results for file1 and file2 under the same common column value
                results.append({
                    'common_column_value': common_value,
                    'file_name': file1_name,
                    'combined_column_data': data_file1,
                    'status': status,
                    'description': description
                })
                results.append({
                    'common_column_value': common_value,
                    'file_name': file2_name,
                    'combined_column_data': data_file2,
                    'status': status,
                    'description': description
                })

    return render(request, 'matching/compare_results.html', {
        'results': results,
        'comparison': comparison,
        'combined_columns': combined_columns,
    })


