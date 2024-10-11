from django.db import models
from upload.models import ExcelFile


class MatchingResult(models.Model):
    debtor_file = models.ForeignKey(ExcelFile, related_name='debtor_matches', on_delete=models.CASCADE)
    claimer_file = models.ForeignKey(ExcelFile, related_name='claimer_matches', on_delete=models.CASCADE)
    main_column_value = models.CharField(max_length=255)
    matched_data = models.JSONField()  # Stores the matched row data as JSON for better representation.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match Result: {self.main_column_value}"


class MatchingPreset(models.Model):
    name = models.CharField(max_length=100)
    debtor_columns = models.JSONField()  # Stores selected debtor columns for matching
    claimer_columns = models.JSONField()  # Stores selected claimer columns for matching
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Preset: {self.name}"


class MatchingHistory(models.Model):
    preset = models.ForeignKey(MatchingPreset, on_delete=models.SET_NULL, null=True, blank=True)
    debtor_file = models.ForeignKey(ExcelFile, related_name='debtor_history', on_delete=models.CASCADE)
    claimer_file = models.ForeignKey(ExcelFile, related_name='claimer_history', on_delete=models.CASCADE)
    main_column_value = models.CharField(max_length=255)
    matched_data = models.JSONField()  # Stores the matched data as JSON for history purposes.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History: {self.main_column_value} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"