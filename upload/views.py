from django.shortcuts import render, redirect
from .forms import FileUploadForm
from upload.models import ExcelFile, Debtor, Claimer
import pandas as pd
from django.contrib.auth.decorators import login_required


def check_file_type(uploaded_file):
    # Only .xlsx files are allowed
    if not uploaded_file.name.endswith('.xlsx'):
        return False, 'Wrong file type. Only .xlsx files are allowed.'
    return True, None


def read_excel_file(uploaded_file):
    try:
        return pd.read_excel(uploaded_file), None
    except ValueError as e:
        return None, f"Invalid file format: {e}"
    except Exception as e:
        return None, f"Error reading the Excel file: {e}"


def get_expected_columns(location):
    expected_columns = {
        'debtor': [
            'No', 'VN', 'HN', 'CID', 'PatientName', 'sex', 'age', 'National', 'vstdate', 'vsttime',
            'Pdx', 'AuthenCode', 'Pttype', 'PttypeName', 'AccCode', 'AccName', 'Pttype_number', 'HospMain',
            'HospSub', 'Price', 'MustPay', 'Paid', 'debt', 'room_food', 'Artificial', 'medicine', 'Home_Med',
            'Med_sup', 'Blood_Components', 'Lab', 'X_Ray', 'Extra', 'Equipment', 'surgery', 'nurse_serv',
            'dental', 'physical', 'other_treatment', 'other_cost', 'med_extra', 'doctor_cost', 'cost', 'DoctorName'
        ],
        'claimer': [
            'VN', 'Stat', 'Ext', 'Line', 'Hreg', 'HN', 'SessNo', 'BegHd', 'HdMode', 'ClaimAcc', 'Payers',
            'Ep', 'DlzNew', 'Amount', 'HDrate', 'NetTotal', 'importdate', 'importStaff', 'bill'
        ]
    }
    return expected_columns.get(location)


def check_column_names(excel_data, location):
    expected_columns = get_expected_columns(location)
    if not expected_columns:
        return False, 'Invalid location selected.'

    actual_columns = list(excel_data.columns)
    
    if expected_columns != actual_columns:
        mismatches = [
            f'Expected: "{expected}", Got: "{actual}"'
            for expected, actual in zip(expected_columns, actual_columns)
            if expected != actual
        ]

        if len(expected_columns) > len(actual_columns):
            mismatches.append(f'Missing columns: {expected_columns[len(actual_columns):]}')
        elif len(actual_columns) > len(expected_columns):
            mismatches.append(f'Unexpected columns: {actual_columns[len(expected_columns):]}')

        return False, "Mismatched columns: " + "; ".join(mismatches)

    return True, None


def save_debtor_data(user, excel_file, excel_data, patient_type):
    debtor_fields = [
        'No', 'VN', 'HN', 'CID', 'PatientName', 'sex', 'age', 'National', 'vstdate', 'vsttime',
        'Pdx', 'AuthenCode', 'Pttype', 'PttypeName', 'AccCode', 'AccName', 'Pttype_number', 'HospMain',
        'HospSub', 'Price', 'MustPay', 'Paid', 'debt', 'room_food', 'Artificial', 'medicine', 'Home_Med',
        'Med_sup', 'Blood_Components', 'Lab', 'X_Ray', 'Extra', 'Equipment', 'surgery', 'nurse_serv',
        'dental', 'physical', 'other_treatment', 'other_cost', 'med_extra', 'doctor_cost', 'cost', 'DoctorName'
    ]

    for _, row in excel_data.iterrows():
        Debtor.objects.create(
            user=user,
            excelfile=excel_file,
            **{field: row[field] for field in debtor_fields},
            patient_type=patient_type
        )


def save_claimer_data(user, excel_file, excel_data, patient_type):
    claimer_fields = [
        'VN', 'HN', 'Stat', 'Ext', 'Line', 'Hreg', 'SessNo', 'BegHd', 'HdMode', 'ClaimAcc', 'Payers',
        'Ep', 'DlzNew', 'Amount', 'HDrate', 'NetTotal', 'importdate', 'importStaff', 'bill'
    ]

    for _, row in excel_data.iterrows():
        Claimer.objects.create(
            user=user,
            excelfile=excel_file,
            **{field: row[field] for field in claimer_fields},
            patient_type=patient_type
        )


def save_excel_data(user, excel_file, excel_data, location, patient_type):
    if location == 'debtor':
        save_debtor_data(user, excel_file, excel_data, patient_type)
    elif location == 'claimer':
        save_claimer_data(user, excel_file, excel_data, patient_type)


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            location = form.cleaned_data['location']
            patient_type = form.cleaned_data['patient_type']
            user = request.user

            # Validate file type
            is_valid, error_message = check_file_type(uploaded_file)
            if not is_valid:
                return render(request, 'error.html', {'error_message': error_message})

            # Read Excel file
            excel_data, error_message = read_excel_file(uploaded_file)
            if excel_data is None:
                return render(request, 'error.html', {'error_message': error_message})

            # Validate column names
            is_valid, error_message = check_column_names(excel_data, location)
            if not is_valid:
                return render(request, 'error.html', {'error_message': error_message})

            # Save file metadata to the ExcelFile model
            excel_file = ExcelFile.objects.create(
                user=user,
                file=uploaded_file,
                location=location,
                patient_type=patient_type,
            )

            # Save the actual Excel data to the appropriate model
            save_excel_data(user, excel_file, excel_data, location, patient_type)

            return render(request, 'success.html')

    else:
        form = FileUploadForm()

    return render(request, 'upload.html', {'form': form})


@login_required
def history_view(request):
    return render(request, "history.html")


@login_required
def match_view(request):
    return render(request, "match.html")


@login_required
def dashboard_view(request):
    return render(request, "dashboard.html")


def login_view(request):
    return render(request, 'login.html')


@login_required
def result_view(request):
    return render(request, "result.html")
