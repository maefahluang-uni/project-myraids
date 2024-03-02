from django import forms
from .models import DebtorExcelBase


class DataSelectionForm(forms.Form):

    selected_data = forms.ModelMultipleChoiceField(queryset=DebtorExcelBase.objects.all(), widget=forms.CheckboxSelectMultiple)

