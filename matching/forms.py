# matching/forms.py

from django import forms
from upload.models import ExcelFile

class FileSelectionForm(forms.Form):
    """Form for selecting two files to compare."""
    excel_file_1 = forms.ModelChoiceField(queryset=ExcelFile.objects.all(), label="Select First File")
    excel_file_2 = forms.ModelChoiceField(queryset=ExcelFile.objects.all(), label="Select Second File")

    def clean(self):
        cleaned_data = super().clean()
        file1 = cleaned_data.get("excel_file_1")
        file2 = cleaned_data.get("excel_file_2")

        if file1 == file2:
            raise forms.ValidationError("Please select two different files for comparison.")
        return cleaned_data


class ColumnSelectionForm(forms.Form):
    """Form for selecting columns from each file and choosing a common column for alignment."""
    def __init__(self, *args, file1_columns=None, file2_columns=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Create choice lists for each file’s columns
        file1_choices = [(col, col) for col in file1_columns or []]
        file2_choices = [(col, col) for col in file2_columns or []]

        self.fields['columns_file1'] = forms.MultipleChoiceField(
            choices=file1_choices,
            label="Select Columns from First File",
            widget=forms.CheckboxSelectMultiple,
        )
        self.fields['columns_file2'] = forms.MultipleChoiceField(
            choices=file2_choices,
            label="Select Columns from Second File",
            widget=forms.CheckboxSelectMultiple,
        )
        self.fields['common_column'] = forms.ChoiceField(
            choices=[(col, col) for col in (file1_columns or []) if col in (file2_columns or [])],
            label="Select Common Column"
        )

    def clean(self):
        cleaned_data = super().clean()
        columns_file1 = cleaned_data.get("columns_file1")
        columns_file2 = cleaned_data.get("columns_file2")

        if len(columns_file1) != len(columns_file2):
            raise forms.ValidationError("Please select an equal number of columns from both files for comparison.")
        
        return cleaned_data


class ColumnPairingForm(forms.Form):
    """Form for mapping columns between the two selected files for comparison."""
    def __init__(self, *args, columns_file1=None, columns_file2=None, **kwargs):
        super().__init__(*args, **kwargs)
        for col1 in columns_file1:
            self.fields[f"pair_{col1}"] = forms.ChoiceField(
                choices=[(col2, col2) for col2 in columns_file2],
                label=f"Map '{col1}' to"
            )
    
    def clean(self):
        cleaned_data = super().clean()
        selected_pairs = [val for key, val in cleaned_data.items() if key.startswith("pair_")]

        if len(selected_pairs) != len(set(selected_pairs)):
            raise forms.ValidationError("Each column from the second file must be mapped to only one column from the first file.")

        return cleaned_data
