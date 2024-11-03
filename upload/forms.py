from django import forms



LOCATION_CHOICES = [
        ('debtor','Debtor'),
        ('claimer','Claimer'),
    ]

PATIENT_TYPE_CHOICES = [
        ('inpatient','Inpatient'),
        ('outpatient','Outpatient'),
    ]

class FileUploadForm(forms.Form):
    file = forms.FileField(label='Choose file:')
    location = forms.ChoiceField(choices=LOCATION_CHOICES, widget=forms.RadioSelect)
    patient_type = forms.ChoiceField(choices=PATIENT_TYPE_CHOICES, widget=forms.RadioSelect)

