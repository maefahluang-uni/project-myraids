# Generated by Django 5.0.2 on 2024-04-01 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0006_fieldpreset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claimerexcelbase',
            name='No',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='debtorexcelbase',
            name='No',
            field=models.IntegerField(null=True),
        ),
    ]
