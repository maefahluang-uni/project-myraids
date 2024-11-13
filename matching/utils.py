# matching/utils.py

import pandas as pd
from upload.models import ExcelFile

def load_columns_from_file(file_id):
    """
    Load columns from an Excel file and return as a list.
    
    Parameters:
    - file_id (int): The ID of the ExcelFile instance to load.

    Returns:
    - list: Column names as a list.
    - DataFrame: The pandas DataFrame of the Excel file's data.
    """
    file_instance = ExcelFile.objects.get(id=file_id)
    df = pd.read_excel(file_instance.file.path)
    return df.columns.tolist(), df

def validate_equal_column_count(columns_file1, columns_file2):
    """
    Check if the number of columns in two lists is equal.

    Parameters:
    - columns_file1 (list): List of column names from the first file.
    - columns_file2 (list): List of column names from the second file.

    Returns:
    - bool: True if the number of columns is equal, False otherwise.
    """
    return len(columns_file1) == len(columns_file2)

def create_combined_column_names(selected_columns_file1, selected_columns_file2):
    """
    Combine column names from file1 and file2 if they are different, or keep the name if they're the same.
    
    Parameters:
    - selected_columns_file1 (list): List of selected column names from the first file.
    - selected_columns_file2 (list): List of selected column names from the second file.

    Returns:
    - list: A list of combined column names.
    """
    combined_columns = []
    for col1, col2 in zip(selected_columns_file1, selected_columns_file2):
        combined_name = f"{col1} - {col2}" if col1 != col2 else col1
        combined_columns.append(combined_name)
    return combined_columns
