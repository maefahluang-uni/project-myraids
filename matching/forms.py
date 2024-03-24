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
        presets = kwargs.pop('presets', {})
        super(ColumnMappingForm, self).__init__(*args, **kwargs)

        self.fields['preset_choice'] = forms.ChoiceField(
            label="Select Preset",
            choices=[('', 'Select Preset')] + [(preset_name, preset_name) for preset_name in presets.keys()],
            required=False,
        )

        for column in excel_columns:
            self.fields[column] = forms.ChoiceField(
                label=column,
                choices=[('', 'Select Model Field')] + [(field_name, field_label) for field_name, field_label in model_fields.items()]
            )

        self.presets = presets

    def update_fields_with_preset(self, preset_name):
        preset_mapping = self.presets.get(preset_name, {})
        for field_name, choices in preset_mapping.items():
            if field_name in self.fields:
                self.fields[field_name].choices = [(choice, choice) for choice in choices]
