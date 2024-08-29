from django.db import models

class ComparisonResult(models.Model):
    debtor_id = models.IntegerField(null=True)
    claimer_id = models.IntegerField(null=True)
    debtor_data = models.JSONField(null=True)  # Store debtor data as JSON
    claimer_data = models.JSONField(null=True)  # Store claimer data as JSON
    status = models.CharField(max_length=10,null=True)  # Green, Yellow, Red
    description = models.TextField(null=True)  # Explanation of the comparison result
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comparison Result {self.id} - Status: {self.status}"
    
