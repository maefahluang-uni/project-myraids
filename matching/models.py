# models.py

import logging
from django.db import models
from django.contrib.auth.models import User
from upload.models import ExcelFile  # Importing from upload app

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class SelectedColumns(models.Model):
    """
    Model to store information about selected columns from two Excel files
    for matching purposes, including common and specific columns.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    excel_file_1 = models.ForeignKey(ExcelFile, on_delete=models.CASCADE, related_name='file1')
    excel_file_2 = models.ForeignKey(ExcelFile, on_delete=models.CASCADE, related_name='file2')
    common_column = models.CharField(max_length=100)
    columns_file1 = models.JSONField()  # List of columns from file 1
    columns_file2 = models.JSONField()  # List of columns from file 2
    created_at = models.DateTimeField(auto_now_add=True)  # New field to track creation date

    def __str__(self):
        return f"Selected columns for matching by {self.user}"

    def save(self, *args, **kwargs):
        # Log action on save
        logger.debug(f"Saving SelectedColumns: user={self.user}, "
                     f"file1={self.excel_file_1}, file2={self.excel_file_2}, "
                     f"common_column={self.common_column}")
        super().save(*args, **kwargs)


class MatchedResult(models.Model):
    """
    Model to store individual matched results between two files based on 
    the selected common column and paired columns.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(SelectedColumns, on_delete=models.CASCADE, related_name='matched_results')
    common_value = models.CharField(max_length=255)  # Value in the common column used for matching
    file_source = models.CharField(max_length=50, choices=[('file1', 'File 1'), ('file2', 'File 2')])
    column_data = models.JSONField()  # Dictionary to store paired column data from each file

    def __str__(self):
        return f"Matched result for {self.common_value} from {self.file_source}"

    def save(self, *args, **kwargs):
        # Log action on save
        logger.debug(f"Saving MatchedResult: user={self.user}, session={self.session}, "
                     f"common_value={self.common_value}, file_source={self.file_source}")
        super().save(*args, **kwargs)
