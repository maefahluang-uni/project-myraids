from django.shortcuts import render
from .forms import FileUploadForm
from upload.models import ExcelFile, Debtor, Claimer
import pandas as pd
from django.contrib.auth.decorators import login_required

def check_file_type(uploaded_file):
    # Check for file type
    if not uploaded_file.name.endswith('.xlsx'):
        return False, 'Wrong file type. Only .xlsx files are allowed.'
    return True, None

def read_excel_file(uploaded_file):
    # Read the uploaded Excel file
    try:
        excel_data = pd.read_excel(uploaded_file)
        return excel_data, None
    except Exception as e:
        return None, f'Error reading Excel file: {e}'

def check_column_names(excel_data, location):
    # Define expected columns for debtor and claimer
    expected_columns = {
        'debtor': [
            'No', 'VN', 'HN', 'CID', 'PatientName', 'sex', 'age', 'National', 'vstdate', 'vsttime',
            'Pdx', 'AuthenCode', 'Pttype', 'PttypeName', 'AccCode', 'AccName', 'Pttype_number', 'HospMain',
            'HospSub', 'Price', 'MustPay', 'Paid', 'debt', 'room_food', 'Artificial', 'medicine', 'Home_Med',
            'Med_sup', 'Blood_Components', 'Lab', 'X_Ray', 'Extra', 'Equipment', 'surgery', 'nurse_serv',
            'dental', 'physical', 'other_treatment', 'other_cost', 'med_extra', 'doctor_cost', 'cost', 'DoctorName'
        ],
        'claimer': [
            'VN','Stat', 'Ext', 'Line', 'Hreg', 'HN',  'SessNo', 'BegHd', 'HdMode', 'ClaimAcc', 'Payers',
            'Ep', 'DlzNew', 'Amount', 'HDrate', 'NetTotal', 'importdate', 'importStaff', 'bill'
        ]
    }

    if location not in expected_columns:
        return False, 'Invalid location selected.'

    # Check if the column names match
    expected = expected_columns[location]
    actual = list(excel_data.columns)

    if expected != actual:
        mismatched_columns = [
            f'Expected: "{expected[i]}", Got: "{actual[i]}"'
            for i in range(min(len(expected), len(actual)))
            if expected[i] != actual[i]
        ]
        if len(expected) > len(actual):
            mismatched_columns.append(f'Missing columns: {expected[len(actual):]}')
        elif len(actual) > len(expected):
            mismatched_columns.append(f'Unexpected columns: {actual[len(expected):]}')

        return False, (
            'The column names are not the same as expected. Mismatched columns:'.join(mismatched_columns)
        )

    return True, None

def save_excel_data(user, excel_file, excel_data, location, patient_type):
    # Save the Excel data to either the Debtor or Claimer model
    if location == 'debtor':
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
                ExcelFile=excel_file,
                **{field: row[field] for field in debtor_fields},
                location=location,
                patient_type=patient_type
            )
    elif location == 'claimer':
        claimer_fields = [
            'VN', 'HN', 'Stat', 'Ext', 'Line', 'Hreg', 'SessNo', 'BegHd', 'HdMode', 'ClaimAcc', 'Payers',
            'Ep', 'DlzNew', 'Amount', 'HDrate', 'NetTotal', 'importdate', 'importStaff', 'bill'
        ]
        for _, row in excel_data.iterrows():
            Claimer.objects.create(
                user=user,
                ExcelFile=excel_file,
                **{field: row[field] for field in claimer_fields},
                location=location,
                patient_type=patient_type
            )

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            location = form.cleaned_data['location']
            patient_type = form.cleaned_data['patient_type']
            user = request.user

            # Check file type
            is_valid, error_message = check_file_type(uploaded_file)
            if not is_valid:
                return render(request, 'error.html', {'error_message': error_message})

            # Read the Excel file
            excel_data, error_message = read_excel_file(uploaded_file)
            if excel_data is None:
                return render(request, 'error.html', {'error_message': error_message})

            # Check column names
            is_valid, error_message = check_column_names(excel_data, location)
            if not is_valid:
                return render(request, 'error.html', {'error_message': error_message})

            # Save metadata to ExcelFile model without storing the actual file
            excel_file = ExcelFile.objects.create(
                user=user,
                file=uploaded_file,  # This stores the reference, but no actual file storage in system.
                location=location,
                patient_type=patient_type,
            )

            # Save the Excel data to the appropriate model
            save_excel_data(user, excel_file, excel_data, location, patient_type)

            return render(request, 'success.html')
    else:
        form = FileUploadForm()

    return render(request, 'upload.html', {'form': form})

def history_view(request):
    return render(request, "history.html")

def match_view(request):
    return render(request, "match.html")

def dashboard_view(request):
    return render(request, "dashboard.html")

def login_view(request):
    return render(request, 'login.html')    

def result_view(request):
    return render(request,"result.html")

