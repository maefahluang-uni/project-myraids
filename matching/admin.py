from django.contrib import admin
from django import forms
from .models import DebtorExcelBase, ClaimerExcelBase, FieldPreset

class FieldPresetForm(forms.ModelForm):
    class Meta:
        model = FieldPreset
        fields = '__all__'
        widgets = {
            'preset_data': forms.Textarea(attrs={'rows': 20, 'cols': 80})  # Adjust size as needed
        }

@admin.register(DebtorExcelBase)
class DebtorExcelBaseAdmin(admin.ModelAdmin):
    list_display = ('No', 'AN', 'HN', 'CID', 'name', 'admit_date', 'left_date', 'total_days', 'Pdx', 'AdjRw', 'AuthenCode', 'Pttype', 'claim_catg', 'claim_folname', 'HospMain', 'HospSub', 'p_chart_status', 'expense_fee', 'amount_tobe_paid_fee', 'amount_paid_fee', 'debt_left_fee', 'room_food_fee', 'drug_fee', 'takehome_drug_fee', 'medical_supplie_fee', 'bloodcomponent_fee', 'Lab_fee', 'X_Ray_fee', 'special_inspection_fee', 'equipment_fee', 'procedure_fee', 'nursing_fee', 'dental_fee', 'physicaltharapy_fee', 'othertharapy_fee', 'other_fee', 'not_insure_fee', 'doctor_fee', 'total_fee')
    search_fields = ('No', 'AN', 'HN', 'CID', 'name', 'claim_catg', 'claim_folname', 'HospMain', 'HospSub')
    list_filter = ('admit_date', 'left_date', 'Pttype')

@admin.register(ClaimerExcelBase)
class ClaimerExcelBaseAdmin(admin.ModelAdmin):
    list_display = ('No', 'AN', 'HN', 'CID', 'name', 'admit_date', 'left_date', 'total_days', 'Pdx', 'AdjRw', 'AuthenCode', 'Pttype', 'claim_catg', 'claim_folname', 'HospMain', 'HospSub', 'p_chart_status', 'expense_fee', 'amount_tobe_paid_fee', 'amount_paid_fee', 'debt_left_fee', 'room_food_fee', 'drug_fee', 'takehome_drug_fee', 'medical_supplie_fee', 'bloodcomponent_fee', 'Lab_fee', 'X_Ray_fee', 'special_inspection_fee', 'equipment_fee', 'procedure_fee', 'nursing_fee', 'dental_fee', 'physicaltharapy_fee', 'othertharapy_fee', 'other_fee', 'not_insure_fee', 'doctor_fee', 'total_fee')
    search_fields = ('No', 'AN', 'HN', 'CID', 'name', 'claim_catg', 'claim_folname', 'HospMain', 'HospSub')
    list_filter = ('admit_date', 'left_date', 'Pttype')

@admin.register(FieldPreset)
class FieldPresetAdmin(admin.ModelAdmin):
    form = FieldPresetForm
    list_display = ('name',)
    search_fields = ('name',)