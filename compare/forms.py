from django import forms
from matching.models import DebtorExcelBase, ClaimerExcelBase

class ComparisonForm(forms.Form):
    # Extract field choices for DebtorExcelBase
    DEBTOR_CHOICES = [(field.name, field.verbose_name) for field in DebtorExcelBase._meta.get_fields() if field.name not in ['id']]

    # Extract field choices for ClaimerExcelBase
    CLAIMER_CHOICES = [(field.name, field.verbose_name) for field in ClaimerExcelBase._meta.get_fields() if field.name not in ['id']]

    key_columns = forms.MultipleChoiceField(
        label='Select Key Columns',
        choices=DEBTOR_CHOICES + CLAIMER_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text="Select columns that should be used as keys for matching records."
    )

    non_key_columns = forms.MultipleChoiceField(
        label='Select Non-Key Columns to Compare',
        choices=DEBTOR_CHOICES + CLAIMER_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text="Select columns for detailed comparison."
    )
