from django import forms
from upload.models import ExcelFile, Debtor, Claimer


class DebtorForm(forms.Form):
    debtor_file = forms.ModelChoiceField(queryset=ExcelFile.objects.filter(location='debtor'), label="Select Debtor File")
    main_column = forms.ChoiceField(label="Main Column for Matching (Debtor)", choices=[], widget=forms.Select)
    selected_columns = forms.MultipleChoiceField(label="Select Columns for Matching (Debtor)", choices=[], widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(DebtorForm, self).__init__(*args, **kwargs)
        # Dynamic choices for debtor columns based on Debtor model fields
        debtor_fields = [(field.name, f"Debtor: {field.verbose_name}") for field in Debtor._meta.get_fields() if field.name not in ['id', 'user', 'ExcelFile']]
        self.fields['main_column'].choices = debtor_fields
        self.fields['selected_columns'].choices = debtor_fields


class ClaimerForm(forms.Form):
    claimer_file = forms.ModelChoiceField(queryset=ExcelFile.objects.filter(location='claimer'), label="Select Claimer File")
    main_column = forms.ChoiceField(label="Main Column for Matching (Claimer)", choices=[], widget=forms.Select)
    selected_columns = forms.MultipleChoiceField(label="Select Columns for Matching (Claimer)", choices=[], widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(ClaimerForm, self).__init__(*args, **kwargs)
        # Dynamic choices for claimer columns based on Claimer model fields
        claimer_fields = [(field.name, f"Claimer: {field.verbose_name}") for field in Claimer._meta.get_fields() if field.name not in ['id', 'user', 'ExcelFile']]
        self.fields['main_column'].choices = claimer_fields
        self.fields['selected_columns'].choices = claimer_fields


class MatchingForm(forms.Form):
    debtor_main_column = forms.ChoiceField(label="Main Column for Matching (Debtor)", choices=[], widget=forms.Select)
    claimer_main_column = forms.ChoiceField(label="Main Column for Matching (Claimer)", choices=[], widget=forms.Select)
    debtor_selected_columns = forms.MultipleChoiceField(label="Select Columns for Matching (Debtor)", choices=[], widget=forms.CheckboxSelectMultiple)
    claimer_selected_columns = forms.MultipleChoiceField(label="Select Columns for Matching (Claimer)", choices=[], widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(MatchingForm, self).__init__(*args, **kwargs)
        # Dynamic choices for debtor and claimer columns based on respective model fields
        debtor_fields = [(field.name, f"Debtor: {field.verbose_name}") for field in Debtor._meta.get_fields() if field.name not in ['id', 'user', 'ExcelFile']]
        claimer_fields = [(field.name, f"Claimer: {field.verbose_name}") for field in Claimer._meta.get_fields() if field.name not in ['id', 'user', 'ExcelFile']]
        
        self.fields['debtor_main_column'].choices = debtor_fields
        self.fields['claimer_main_column'].choices = claimer_fields
        self.fields['debtor_selected_columns'].choices = debtor_fields
        self.fields['claimer_selected_columns'].choices = claimer_fields


class PresetForm(forms.Form):
    preset_name = forms.CharField(label="Preset Name", max_length=100, widget=forms.TextInput(attrs={
        'id': 'preset_name',
    }))
    debtor_file = forms.ModelChoiceField(queryset=ExcelFile.objects.filter(location='debtor'), label="Select Debtor File", widget=forms.Select(attrs={
        'id': 'debtor_file',
    }))
    claimer_file = forms.ModelChoiceField(queryset=ExcelFile.objects.filter(location='claimer'), label="Select Claimer File", widget=forms.Select(attrs={
        'id': 'claimer_file',
    }))
    debtor_main_column = forms.ChoiceField(label="Main Column for Matching (Debtor)", choices=[], widget=forms.Select(attrs={
        'id': 'debtor_main_column',
    }))
    claimer_main_column = forms.ChoiceField(label="Main Column for Matching (Claimer)", choices=[], widget=forms.Select(attrs={
        'id': 'claimer_main_column',
    }))
    debtor_selected_columns = forms.MultipleChoiceField(label="Select Columns for Matching (Debtor)", choices=[], widget=forms.CheckboxSelectMultiple(attrs={
        'id': 'debtor_selected_columns',
    }))
    claimer_selected_columns = forms.MultipleChoiceField(label="Select Columns for Matching (Claimer)", choices=[], widget=forms.CheckboxSelectMultiple(attrs={
        'id': 'claimer_selected_columns',
    }))

    def __init__(self, *args, **kwargs):
        super(PresetForm, self).__init__(*args, **kwargs)
        # Dynamic choices for debtor and claimer columns based on respective model fields
        debtor_fields = [(field.name, f"Debtor: {field.verbose_name}") for field in Debtor._meta.get_fields() if field.name not in ['id', 'user', 'ExcelFile']]
        claimer_fields = [(field.name, f"Claimer: {field.verbose_name}") for field in Claimer._meta.get_fields() if field.name not in ['id', 'user', 'ExcelFile']]
        
        self.fields['debtor_main_column'].choices = debtor_fields
        self.fields['claimer_main_column'].choices = claimer_fields
        self.fields['debtor_selected_columns'].choices = debtor_fields
        self.fields['claimer_selected_columns'].choices = claimer_fields