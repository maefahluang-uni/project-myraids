# upload/apps.py

from django.apps import AppConfig

class UploadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'upload'

    def ready(self):
        # Import the signals module to connect the signal handlers
        import upload.signals
