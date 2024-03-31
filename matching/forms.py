from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _
from .models import DebtorExcelBase, ClaimerExcelBase

class DataSelectionForm(forms.Form):

    selected_data = forms.ModelMultipleChoiceField(queryset=DebtorExcelBase.objects.all(), widget=forms.CheckboxSelectMultiple)

class ColumnMappingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        excel_columns = kwargs.pop('excel_columns', [])
        model_fields = kwargs.pop('model_fields', {})
        super(ColumnMappingForm, self).__init__(*args, **kwargs)

        for column in excel_columns:
            self.fields[column] = forms.ChoiceField(
                label=column,
                choices=[('', 'Select Model Field')] + [(field_name, field_label) for field_name, field_label in model_fields.items()]
            )

