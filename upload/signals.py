# upload/signals.py

import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import ExcelFile

@receiver(post_delete, sender=ExcelFile)
def delete_file_on_model_delete(sender, instance, **kwargs):
    # Delete the file from the filesystem
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
