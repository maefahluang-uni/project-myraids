from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from upload.models import ExcelFile, Debtor, Claimer
from .forms import DebtorForm, ClaimerForm, MatchingForm, PresetForm
from .models import MatchingResult, MatchingPreset, MatchingHistory
import pandas as pd
from django.contrib import messages
from django.contrib.auth.models import User
from collections import Counter
import datetime
from django.db import models


@login_required
def home(request):
    # Use distinct to count unique ExcelFile records associated with debtors and claimers
    total_debtors = Debtor.objects.values('ExcelFile').distinct().count()
    total_claimers = Claimer.objects.values('ExcelFile').distinct().count()
    total_users = User.objects.count()
    total_uploaded_files = ExcelFile.objects.count()

    total_matching_results = MatchingResult.objects.count()

    uploaded_files_by_month = (
        MatchingResult.objects
        .extra(select={'month': "EXTRACT(MONTH FROM created_at)"})
        .values('month')
        .annotate(count=models.Count('id'))
    )
    
    # Create a dictionary for month and count
    uploaded_files_by_month_dict = {entry['month']: entry['count'] for entry in uploaded_files_by_month}

    context = {
        'total_debtors': total_debtors,
        'total_claimers': total_claimers,
        'total_users': total_users,
        'total_uploaded_files': total_uploaded_files,
        'total_matching_results': total_matching_results,
        'uploaded_files_by_month': uploaded_files_by_month_dict,
    }
    return render(request, 'matching/home.html', context)

@login_required
def select_files_for_matching(request):
    # Step 1: Select files for matching
    if request.method == 'POST':
        debtor_file_id = request.POST.get('debtor_file')
        claimer_file_id = request.POST.get('claimer_file')

        if debtor_file_id and claimer_file_id:
            request.session['debtor_file_id'] = debtor_file_id
            request.session['claimer_file_id'] = claimer_file_id
            return redirect('select_columns_for_matching')
    
    debtor_files = ExcelFile.objects.filter(location='debtor')
    claimer_files = ExcelFile.objects.filter(location='claimer')

    return render(request, 'matching/select_files.html', {
        'debtor_files': debtor_files,
        'claimer_files': claimer_files,
    })


@login_required
def select_columns_for_matching(request):
    # Step 2: Select columns for matching
    debtor_file_id = request.session.get('debtor_file_id')
    claimer_file_id = request.session.get('claimer_file_id')

    if not debtor_file_id or not claimer_file_id:
        messages.error(request, "Please select files first.")
        return redirect('select_files_for_matching')

    debtor_file = get_object_or_404(ExcelFile, id=debtor_file_id)
    claimer_file = get_object_or_404(ExcelFile, id=claimer_file_id)

    if request.method == 'POST':
        form = MatchingForm(request.POST)
        if form.is_valid():
            # Get selected columns for matching
            debtor_main_column = form.cleaned_data['debtor_main_column']
            claimer_main_column = form.cleaned_data['claimer_main_column']
            debtor_selected_columns = form.cleaned_data['debtor_selected_columns']
            claimer_selected_columns = form.cleaned_data['claimer_selected_columns']

            try:
                # Load data from Debtor and Claimer models
                debtor_data = Debtor.objects.filter(ExcelFile=debtor_file).values()
                claimer_data = Claimer.objects.filter(ExcelFile=claimer_file).values()

                # Convert to DataFrames for matching
                debtor_df = pd.DataFrame(debtor_data)
                claimer_df = pd.DataFrame(claimer_data)

                # Perform matching based on the main columns and selected columns
                matched_data = pd.merge(
                    debtor_df,
                    claimer_df,
                    left_on=debtor_main_column,
                    right_on=claimer_main_column,
                    suffixes=('_debtor', '_claimer')
                )

                # Filter only the selected columns for output
                matched_columns = [
                    f'{col}_debtor' for col in debtor_selected_columns
                ] + [
                    f'{col}_claimer' for col in claimer_selected_columns
                ]
                matched_result = matched_data[[debtor_main_column, claimer_main_column] + matched_columns]

                # Convert the result to a list of dictionaries for rendering
                result_list = matched_result.to_dict(orient='records')

                # Save the matching result to the database
                for row in result_list:
                    MatchingResult.objects.create(
                        debtor_file=debtor_file,
                        claimer_file=claimer_file,
                        main_column_value=row[debtor_main_column],
                        matched_data=row
                    )

                return render(request, 'matching/match_result.html', {'result_list': result_list})
            except KeyError as e:
                messages.error(request, f"Column not found: {str(e)}. Please check your selected files and columns.")
                return redirect('select_columns_for_matching')
            except Exception as e:
                messages.error(request, f"An error occurred during matching: {str(e)}")
                return redirect('select_columns_for_matching')
    else:
        form = MatchingForm()

    return render(request, 'matching/select_columns.html', {
        'form': form,
        'debtor_file': debtor_file,
        'claimer_file': claimer_file,
    })


def view_matching_results(request):
    # Fetch all saved matching results
    matching_results = MatchingResult.objects.all()
    return render(request, 'matching/view_results.html', {'matching_results': matching_results})


def view_matching_history(request):
    # Fetch all matching history records
    matching_history = MatchingHistory.objects.all()
    return render(request, 'matching/view_history.html', {'matching_history': matching_history})


def create_matching_preset(request):
    if request.method == 'POST':
        form = PresetForm(request.POST)
        if form.is_valid():
            # Get selected files and main columns for the preset
            name = form.cleaned_data['preset_name']
            debtor_file = form.cleaned_data['debtor_file']
            claimer_file = form.cleaned_data['claimer_file']
            debtor_main_column = form.cleaned_data['debtor_main_column']
            claimer_main_column = form.cleaned_data['claimer_main_column']
            debtor_selected_columns = form.cleaned_data['debtor_selected_columns']
            claimer_selected_columns = form.cleaned_data['claimer_selected_columns']

            # Create a new MatchingPreset
            try:
                preset = MatchingPreset.objects.create(
                    name=name,
                    debtor_columns=debtor_selected_columns,
                    claimer_columns=claimer_selected_columns
                )
                messages.success(request, f"Preset '{name}' created successfully.")
            except Exception as e:
                messages.error(request, f"An error occurred while creating the preset: {str(e)}")
                return redirect('create_matching_preset')

            return redirect('home')
    else:
        form = PresetForm()

    return render(request, 'matching/create_preset.html', {'form': form})
