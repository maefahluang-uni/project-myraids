from django import forms



LOCATION_CHOICES = [
        ('debtor','Debtor'),
        ('claimer','Claimer'),
    ]

PATEINT_TYPE_CHOICES = [
        ('inpatient','Inpatient'),
        ('outpatient','Outpatient'),
    ]

class FileUploadForm(forms.Form):
    file = forms.FileField(label='Choose file:')
    location = forms.ChoiceField(choices=LOCATION_CHOICES, widget=forms.RadioSelect)
    patient_type = forms.ChoiceField(choices=PATEINT_TYPE_CHOICES, widget=forms.RadioSelect)

