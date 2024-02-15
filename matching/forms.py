from django import forms
from .models import ExcelBase

class DataSelectionForm(forms.Form):
    selected_data = forms.ModelMultipleChoiceField(queryset=ExcelBase.objects.all(), widget=forms.CheckboxSelectMultiple)
