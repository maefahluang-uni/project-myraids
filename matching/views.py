# matching/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Comparison, ColumnSelection, ComparisonResult
from .forms import FileSelectionForm, ColumnSelectionForm, ColumnPairingForm
from .utils import load_columns_from_file, create_combined_column_names
from upload.models import ExcelFile, Debtor, Claimer
from .models import MatchingResult, MatchingPreset, MatchingHistory
import pandas as pd
from django.contrib import messages
from django.contrib.auth.models import User
from collections import Counter
import datetime
from django.db import models
from django.http import HttpResponseForbidden
from .models import ComparisonResult


@login_required
def home(request):
    # Use distinct to count unique ExcelFile records associated with debtors and claimers
    total_debtors = Debtor.objects.values('excelfile').distinct().count()
    total_claimers = Claimer.objects.values('excelfile').distinct().count()  # Changed to excelfile (lowercase)
    total_users = User.objects.count()
    total_comparisons = Comparison.objects.count()
    total_matching_results = MatchingResult.objects.count()

    

    uploaded_files_by_month = (
        MatchingResult.objects
        .extra(select={'month': "EXTRACT(MONTH FROM created_at)"})
        .values('month')
        .annotate(count=models.Count('id'))
        .order_by('month')
    )
    
    # Create a dictionary for month and count
    uploaded_files_by_month_dict = {entry['month']: entry['count'] for entry in uploaded_files_by_month}

    
    context = {
        'total_debtors': total_debtors,
        'total_claimers': total_claimers,
        'total_users': total_users,
        'total_comparisons': total_comparisons,
        'total_matching_results': total_matching_results,
        'uploaded_files_by_month': uploaded_files_by_month_dict,
    }
    return render(request, 'matching/home.html', context)

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

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Comparison
from .utils import load_columns_from_file

@login_required
def compare_results(request, comparison_id):
    """View to display the results of the comparison."""
    comparison = get_object_or_404(Comparison, id=comparison_id, user=request.user)
    column_selections = comparison.column_selections.all()

    # Load dataframes for comparison
    file1_id, file2_id = comparison.file1.id, comparison.file2.id
    _, df1 = load_columns_from_file(file1_id)
    _, df2 = load_columns_from_file(file2_id)

    # Retrieve instance names and common column
    file1_name, file2_name = str(comparison.file1), str(comparison.file2)
    common_column = comparison.common_column

    # Generate column mappings for file1 and file2
    file1_columns = [sel.column_file1 for sel in column_selections]
    file2_columns = [sel.column_file2 for sel in column_selections]
    combined_columns = [f"{sel.column_file1}_{sel.column_file2}" for sel in column_selections]

    # Prepare data for the two views
    results_combined_view = []
    results_side_by_side = []

    for _, row1 in df1.iterrows():
        for _, row2 in df2.iterrows():
            if row1[common_column] == row2[common_column]:
                common_value = row1[common_column]
                
                # Data for combined view
                data_file1 = {f"{sel.column_file1}_{sel.column_file2}": row1[sel.column_file1] for sel in column_selections}
                data_file2 = {f"{sel.column_file1}_{sel.column_file2}": row2[sel.column_file2] for sel in column_selections}
                combined_status = 'Match' if data_file1 == data_file2 else 'Mismatch'
                description = 'All data matches' if combined_status == 'Match' else 'Data differs'

                results_combined_view.append({
                    'common_column_value': common_value,
                    'file_name': file1_name,
                    'combined_column_data': data_file1,
                    'status': combined_status,
                    'description': description
                })
                results_combined_view.append({
                    'common_column_value': common_value,
                    'file_name': file2_name,
                    'combined_column_data': data_file2,
                    'status': combined_status,
                    'description': description
                })

                # Data for side-by-side view
                side_by_side_data_file1 = {col: row1[col] for col in file1_columns}
                side_by_side_data_file2 = {col: row2[col] for col in file2_columns}
                side_by_side_status = 'Match' if side_by_side_data_file1 == side_by_side_data_file2 else 'Mismatch'
                
                results_side_by_side.append({
                    'common_column_value': common_value,
                    'file1_data': side_by_side_data_file1,
                    'file2_data': side_by_side_data_file2,
                    'status': side_by_side_status,
                    'description': description
                })

    return render(request, 'matching/compare_results.html', {
        'results_combined_view': results_combined_view,
        'results_side_by_side': results_side_by_side,
        'file1_name': file1_name,
        'file2_name': file2_name,
        'file1_columns': file1_columns,
        'file2_columns': file2_columns,
        'combined_columns': combined_columns,
    })

def view_matching_results(request):
    # Fetch all saved matching results
    matching_results = MatchingResult.objects.all()
    return render(request, 'matching/view_results.html', {'matching_results': matching_results})


def view_matching_history(request):
    # Fetch all matching history records
    matching_history = MatchingHistory.objects.all()
    comparisons = Comparison.objects.filter(user=request.user)

    context = {
        'comparisons': comparisons,
    }
    return render(request, 'matching/view_history.html', context)

@login_required
def delete_result(request, result_id):
    """View to delete a specific result."""
    result = get_object_or_404(ComparisonResult, id=result_id)

    if result.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this item.")

    result.delete()
    messages.success(request, "Row deleted successfully.")
    return redirect('matching:comparison_results')
