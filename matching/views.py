# views.py

import logging
from django.db.models import Q
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FileSelectionForm, ColumnSelectionForm, ColumnPairingForm
from .models import SelectedColumns, MatchedResult
from upload.models import ExcelFile,Debtor,Claimer
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@login_required
def home(request):
    sessions = SelectedColumns.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'matching/home.html', {'sessions': sessions})


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_columns_from_model(model_class):
    return [field.name for field in model_class._meta.fields if field.name != 'id']



@login_required
def file_selection_view(request):
    if request.method == 'POST':
        form = FileSelectionForm(request.POST)
        if form.is_valid():
            # Get the selected files and save necessary details to the session
            file1 = form.cleaned_data['excel_file_1']
            file2 = form.cleaned_data['excel_file_2']

            # Save IDs and patient/location data in session for subsequent steps
            request.session['file1_id'] = file1.id
            request.session['file2_id'] = file2.id
            request.session['patient_type_1'] = file1.patient_type
            request.session['location_1'] = file1.location
            request.session['patient_type_2'] = file2.patient_type
            request.session['location_2'] = file2.location

            return redirect('matching:column_selection')
    else:
        form = FileSelectionForm()
    return render(request, 'matching/file_selection.html', {'form': form})

@login_required
def column_selection_view(request):
    # Retrieve file IDs from session
    file1_id = request.session.get('file1_id')
    file2_id = request.session.get('file2_id')

    # Check if both files are selected
    if not file1_id or not file2_id:
        messages.error(request, "Please select files first.")
        return redirect('matching:file_selection')

    # Retrieve the ExcelFile instances
    file1 = ExcelFile.objects.get(id=file1_id)
    file2 = ExcelFile.objects.get(id=file2_id)

    # Determine columns for each file without patient type or location dependency
    file1_columns = get_columns_from_model(Debtor if file1.debtors.exists() else Claimer)
    file2_columns = get_columns_from_model(Debtor if file2.debtors.exists() else Claimer)

    # Handle POST request
    if request.method == 'POST':
        form = ColumnSelectionForm(request.POST, file1_columns=file1_columns, file2_columns=file2_columns)
        if form.is_valid():
            # Store selected columns in session for later steps
            request.session['columns_file1'] = form.cleaned_data['columns_file1']
            request.session['columns_file2'] = form.cleaned_data['columns_file2']
            request.session['common_column'] = form.cleaned_data['common_column']
            return redirect('matching:column_pairing')
    else:
        # Initialize form with columns from each file
        form = ColumnSelectionForm(file1_columns=file1_columns, file2_columns=file2_columns)

    return render(request, 'matching/column_selection.html', {
        'form': form,
        'file1': file1,
        'file2': file2
    })

@login_required
def column_pairing_view(request):
    selected_columns_file1 = request.session.get('columns_file1')
    selected_columns_file2 = request.session.get('columns_file2')

    if not selected_columns_file1 or not selected_columns_file2:
        messages.error(request, "Please complete the column selection step first.")
        logger.debug("Column selection data missing; redirecting to column selection.")
        return redirect('matching:column_selection')

    if request.method == 'POST':
        form = ColumnPairingForm(request.POST, columns_file1=selected_columns_file1, columns_file2=selected_columns_file2)
        if form.is_valid():
            column_pairs = {
                col1: form.cleaned_data[f"pair_{col1}"]
                for col1 in selected_columns_file1
                if form.cleaned_data.get(f"pair_{col1}")
            }
            request.session['column_pairs'] = column_pairs
            request.session.modified = True  # Ensure session persistence
            logger.debug(f"Column pairs saved to session: {column_pairs}")
            return redirect('matching:match_results')
    else:
        form = ColumnPairingForm(columns_file1=selected_columns_file1, columns_file2=selected_columns_file2)

    return render(request, 'matching/column_pairing.html', {'form': form})


@login_required
def match_results_view(request):
    # Retrieve session data for files and columns
    file1_id = request.session.get('file1_id')
    file2_id = request.session.get('file2_id')
    common_column = request.session.get('common_column')
    column_pairs = request.session.get('column_pairs')

    logger.debug(f"Session data in match_results_view: file1_id={file1_id}, file2_id={file2_id}, "
                 f"common_column={common_column}, column_pairs={column_pairs}")

    if not all([file1_id, file2_id, common_column, column_pairs]):
        messages.error(request, "Required data is missing. Please complete all steps.")
        logger.debug("Missing session data in match_results_view, redirecting to column selection.")
        return redirect('matching:column_selection')
    file1_columns = list(column_pairs.keys())
    file2_columns = list(column_pairs.values())
    
    try:
        # Retrieve ExcelFile instances
        file1 = ExcelFile.objects.get(id=file1_id)
        file2 = ExcelFile.objects.get(id=file2_id)

        # Retrieve data based on the Debtor or Claimer associations
        file1_data = file1.debtors.values(*file1_columns) if file1.debtors.exists() else file1.claimers.values(*file1_columns)
        file2_data = file2.debtors.values(*file2_columns) if file2.debtors.exists() else file2.claimers.values(*file2_columns)

        # Convert data to DataFrames and rename columns for merging
        df1 = pd.DataFrame(file1_data).rename(columns=column_pairs)
        df1['file_source'] = 'file1'
        df2 = pd.DataFrame(file2_data)
        df2['file_source'] = 'file2'

        # Ensure the common column exists in both DataFrames
        if common_column not in df1.columns or common_column not in df2.columns:
            messages.error(request, f"Common column '{common_column}' not found in both files.")
            logger.debug(f"Common column '{common_column}' missing in one or both DataFrames.")
            return redirect('matching:column_selection')

        # Merge DataFrames on the common column
        merged_df = pd.merge(df1, df2, on=common_column, how='outer', indicator=True)
        
        # Log information about the merge result for debugging
        logger.debug(f"Merged DataFrame:\n{merged_df}")

        # Save session details in SelectedColumns
        session = SelectedColumns.objects.create(
            user=request.user,
            excel_file_1=file1,
            excel_file_2=file2,
            common_column=common_column,
            columns_file1=file1_columns,
            columns_file2=file2_columns
        )
        logger.debug(f"SelectedColumns session created with ID {session.id}")

        # Clear any previous matched results for this session
        MatchedResult.objects.filter(session=session).delete()

        # Save each matched result in MatchedResult model
        for _, row in merged_df.iterrows():
            common_value = row[common_column]
            file_source = row['file_source']
            column_data = {col: row[col] for col in column_pairs.keys() if col in row}

            # Save individual matched result
            matched_result = MatchedResult.objects.create(
                user=request.user,
                session=session,
                common_value=common_value,
                file_source=file_source,
                column_data=column_data
            )
            logger.debug(f"MatchedResult created with ID {matched_result.id} for common value '{common_value}'")

        # Redirect to a separate view for displaying the results
        return redirect('matching:display_results', session_id=session.id)

    except ExcelFile.DoesNotExist:
        messages.error(request, "One or both selected files could not be found.")
        logger.debug("ExcelFile not found in match_results_view.")
        return redirect('matching:file_selection')
    except ValueError as e:
        messages.error(request, str(e))
        logger.debug(f"ValueError: {str(e)}")
        return redirect('matching:file_selection')
    except Exception as e:
        messages.error(request, f"An error occurred while processing the files: {str(e)}")
        logger.debug(f"Unexpected error in match_results_view: {str(e)}")
        return redirect('matching:file_selection')
    


@login_required
def display_results(request, session_id):
    try:
        # Retrieve the session and associated matched results
        session = SelectedColumns.objects.get(id=session_id, user=request.user)
        matched_results = MatchedResult.objects.filter(session=session).order_by('common_value', 'file_source')

        # Log matched results to confirm data
        logger.debug(f"Displaying results for session {session_id}, matched results count: {matched_results.count()}")

        # Organize data for display
        display_data = {}
        for result in matched_results:
            common_val = result.common_value
            if common_val not in display_data:
                display_data[common_val] = {"file1": {}, "file2": {}}
            display_data[common_val][result.file_source] = result.column_data

        # Render results to the template
        return render(request, 'matching/match_results.html', {
            'display_data': display_data,
            'common_column': session.common_column
        })

    except SelectedColumns.DoesNotExist:
        messages.error(request, "The selected session could not be found.")
        logger.debug("SelectedColumns session not found in display_results.")
        return redirect('matching:home')
    except Exception as e:
        messages.error(request, f"An error occurred while displaying results: {str(e)}")
        logger.debug(f"Unexpected error in display_results: {str(e)}")
        return redirect('matching:home')


