import os
from django.core.files.storage import FileSystemStorage

class NumberedFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        """Override to add a numbered suffix if the file name already exists."""
        
        # Split the base name and extension
        base, ext = os.path.splitext(name)
        counter = 1
        
        # Keep modifying the name until it's unique
        while self.exists(name):
            name = f"{base}_{counter}{ext}"
            counter += 1

        return name
