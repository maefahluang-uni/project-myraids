from django import forms

class FileUploadForm(forms.Form):
    file = forms.FileField(label='Choose file:')
    location_choices = (
        ('debtor', 'Debtor'),
        ('claimer', 'Claimer'),
    )
    location = forms.ChoiceField(choices=location_choices, widget=forms.RadioSelect)

