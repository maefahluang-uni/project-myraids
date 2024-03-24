import os, json
import pandas as pd
from django.db import models
from django.conf import settings
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponseRedirect,JsonResponse
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

        model_field_presets = {
    'Claimer': {
                'ที่': ['No'],
                'AN': ['AN'],
                'HN': ['HN'],
                'CID': ['CID'],
                'ชื่อผู้ป่วย': ['name'],
                'สัญชาติ': ['nationality'],
                'วันรับรักษา': ['admit_date'],
                'วันจำหน่าย': ['left_date'],
                'วันนอน': ['total_days'],
                'Pdx': ['Pdx'],
                'AdjRW': ['AdjRw'],
                'AuthenCode': ['AuthenCode'],
                'Pttype': ['Pttype'],
                'ชื่อสิทธิ': ['claim_catg'],
                'รหัสผังบัญชี': ['claim_folname_code'],
                'ชื่อผังบัญชี': ['claim_folname'],
                'เลขที่สิทธิ': ['claim_catg_code'],
                'HospMain': ['HospMain'],
                'HospSub': ['HospSub'],
                'สถานะ': ['p_chart_status'],
                'ค่าใช้จ่าย': ['expense_fee'],
                'ต้องชำระ': ['amount_tobe_paid_fee'],
                'ชำระแล้ว': ['amount_paid_fee'],
                'ภาระหนี้': ['debt_left_fee'],
                'ห้อง/อาหาร': ['room_food_fee'],
                'อวัยวะเทียม': ['prosthetic_fee'],
                'ยา': ['drug_fee'],
                'ยากลับบ้าน': ['takehome_drug_fee'],
                'เวชภัณฑ์': ['medical_supplie_fee'],
                'ส่วนประกอบโลหิต': ['bloodcomponent_fee'],
                'Lab': ['Lab_fee'],
                'X-Ray': ['X_Ray_fee'],
                'ตรวจพิเศษ': ['special_inspection_fee'],
                'ค่าอุปกรณ์': ['equipment_fee'],
                'ค่าหัตถการ': ['procedure_fee'],
                'ค่าพยาบาล': ['nursing_fee'],
                'ค่าทันตกรรม': ['dental_fee'],
                'ค่ากายภาพ': ['physicaltharapy_fee'],
                'ค่าบำบัดอื่น': ['othertharapy_fee'],
                'ค่าอื่น': ['other_fee'],
                'ยานอกบัญชี': ['not_insure_fee'],
                'ค่าแพทย์':[ 'doctor_fee'],
                'รวมทั้งสิ้น': ['total_fee']
    },
    'Debtor': {
                'ที่': ['No'],
                'AN': ['AN'],
                'HN': ['HN'],
                'CID': ['CID'],
                'ชื่อผู้ป่วย': ['name'],
                'สัญชาติ': ['nationality'],
                'วันรับรักษา': ['admit_date'],
                'วันจำหน่าย': ['left_date'],
                'วันนอน': ['total_days'],
                'Pdx': ['Pdx'],
                'AdjRW': ['AdjRw'],
                'AuthenCode': ['AuthenCode'],
                'Pttype': ['Pttype'],
                'ชื่อสิทธิ': ['claim_catg'],
                'รหัสผังบัญชี': ['claim_folname_code'],
                'ชื่อผังบัญชี': ['claim_folname'],
                'เลขที่สิทธิ': ['claim_catg_code'],
                'HospMain': ['HospMain'],
                'HospSub': ['HospSub'],
                'สถานะ': ['p_chart_status'],
                'ค่าใช้จ่าย': ['expense_fee'],
                'ต้องชำระ': ['amount_tobe_paid_fee'],
                'ชำระแล้ว': ['amount_paid_fee'],
                'ภาระหนี้': ['debt_left_fee'],
                'ห้อง/อาหาร': ['room_food_fee'],
                'อวัยวะเทียม': ['prosthetic_fee'],
                'ยา': ['drug_fee'],
                'ยากลับบ้าน': ['takehome_drug_fee'],
                'เวชภัณฑ์': ['medical_supplie_fee'],
                'ส่วนประกอบโลหิต': ['bloodcomponent_fee'],
                'Lab': ['Lab_fee'],
                'X-Ray': ['X_Ray_fee'],
                'ตรวจพิเศษ': ['special_inspection_fee'],
                'ค่าอุปกรณ์': ['equipment_fee'],
                'ค่าหัตถการ': ['procedure_fee'],
                'ค่าพยาบาล': ['nursing_fee'],
                'ค่าทันตกรรม': ['dental_fee'],
                'ค่ากายภาพ': ['physicaltharapy_fee'],
                'ค่าบำบัดอื่น': ['othertharapy_fee'],
                'ค่าอื่น': ['other_fee'],
                'ยานอกบัญชี': ['not_insure_fee'],
                'ค่าแพทย์':[ 'doctor_fee'],
                'รวมทั้งสิ้น': ['total_fee']
    },
}

        if request.method == 'POST':
            form = ColumnMappingForm(request.POST, excel_columns=excel_columns, model_fields=model_fields, presets=model_field_presets)
            if form.is_valid():
                preset_choice = form.cleaned_data['preset_choice']
                if preset_choice:
                    form.update_fields_with_preset(preset_choice)
                    return render(request, 'save_data_form.html', {'form': form})
        else:
            form = ColumnMappingForm(excel_columns=excel_columns, model_fields=model_fields, presets=model_field_presets)

        return render(request, 'save_data_form.html', {'form': form})

    except FileNotFoundError:
        return render(request, 'file_not_found.html', {'error': f'File "{decoded_filename}" not found'}, status=404)







