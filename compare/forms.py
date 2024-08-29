from django import forms
from matching.models import DebtorExcelBase, ClaimerExcelBase

class ComparisonForm(forms.Form):
    # Extract field choices for DebtorExcelBase
    DEBTOR_CHOICES = [(field.name, field.verbose_name) for field in DebtorExcelBase._meta.get_fields() if field.name not in ['id']]

    # Extract field choices for ClaimerExcelBase
    CLAIMER_CHOICES = [(field.name, field.verbose_name) for field in ClaimerExcelBase._meta.get_fields() if field.name not in ['id']]

    debtor_key_columns = forms.MultipleChoiceField(
        label='Select Debtor Key Columns',
        choices=DEBTOR_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )

    claimer_key_columns = forms.MultipleChoiceField(
        label='Select Claimer Key Columns',
        choices=CLAIMER_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )

    debtor_non_key_columns = forms.MultipleChoiceField(
        label='Select Debtor Non-Key Columns to Compare',
        choices=DEBTOR_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )

    claimer_non_key_columns = forms.MultipleChoiceField(
        label='Select Claimer Non-Key Columns to Compare',
        choices=CLAIMER_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
