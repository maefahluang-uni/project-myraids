# Generated by Django 5.0.2 on 2024-10-09 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excelfile',
            name='file',
            field=models.FileField(upload_to='filestorage'),
        ),
    ]
