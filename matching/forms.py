# forms.py

from django import forms
from upload.models import ExcelFile
from upload.forms import LOCATION_CHOICES, PATIENT_TYPE_CHOICES


class FileSelectionForm(forms.Form):
    """
    Step 1: Form for selecting two Excel files from a list.
    """
    excel_file_1 = forms.ModelChoiceField(queryset=ExcelFile.objects.all(), label="Select First Excel File")
    excel_file_2 = forms.ModelChoiceField(queryset=ExcelFile.objects.all(), label="Select Second Excel File")

    def clean(self):
        """
        Ensure that two different files are selected.
        """
        cleaned_data = super().clean()
        file1 = cleaned_data.get('excel_file_1')
        file2 = cleaned_data.get('excel_file_2')

        if file1 == file2:
            raise forms.ValidationError("Please select two different files.")
        
        return cleaned_data

class ColumnSelectionForm(forms.Form):
    """
    Step 2: Form for selecting the common column and specific columns from each file.
    """
    common_column = forms.ChoiceField(label="Select Common Column")
    columns_file1 = forms.MultipleChoiceField(
        label="Columns from First File",
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    columns_file2 = forms.MultipleChoiceField(
        label="Columns from Second File",
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def __init__(self, *args, **kwargs):
        """
        Dynamically populate choices for columns and exclude the common column from 
        the specific column selection options.
        """
        file1_columns = kwargs.pop('file1_columns', [])
        file2_columns = kwargs.pop('file2_columns', [])
        super().__init__(*args, **kwargs)

        # Populate common column choices with columns available in both files
        common_columns = [col for col in file1_columns if col in file2_columns]
        self.fields['common_column'].choices = [(col, col) for col in common_columns]
        
        # Exclude the common column from the specific columns
        self.fields['columns_file1'].choices = [(col, col) for col in file1_columns if col not in common_columns]
        self.fields['columns_file2'].choices = [(col, col) for col in file2_columns if col not in common_columns]


class ColumnPairingForm(forms.Form):
    """
    Step 3: Form for pairing columns from the selected columns of each file.
    Uses dropdowns for each column in File 1 to select a corresponding column from File 2.
    """
    def __init__(self, *args, **kwargs):
        columns_file1 = kwargs.pop('columns_file1', [])
        columns_file2 = kwargs.pop('columns_file2', [])
        super().__init__(*args, **kwargs)

        # Populate dropdown fields for each column in File 1, with choices from columns in File 2
        for col1 in columns_file1:
            self.fields[f"pair_{col1}"] = forms.ChoiceField(
                label=f"Pair for '{col1}'",
                choices=[(col2, col2) for col2 in columns_file2],
                required=False
            )
