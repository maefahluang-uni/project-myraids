# Generated by Django 5.0.2 on 2024-11-14 03:39

import upload.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excelfile',
            name='file',
            field=models.FileField(storage=upload.storage.NumberedFileSystemStorage(), upload_to='filestorage'),
        ),
    ]
