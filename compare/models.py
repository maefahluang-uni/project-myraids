from django.db import models

class ComparisonResult(models.Model):
    debtor_id = models.IntegerField()
    claimer_id = models.IntegerField()
    debtor_data = models.JSONField()  # Store debtor data as JSON
    claimer_data = models.JSONField()  # Store claimer data as JSON
    status = models.CharField(max_length=10)  # Green, Yellow, Red
    description = models.TextField()  # Explanation of the comparison result
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comparison Result {self.id} - Status: {self.status}"
    
