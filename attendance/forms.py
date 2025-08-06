from django import forms

class StudentImportForm(forms.Form):
    file = forms.FileField(label="Select a CSV or Excel file")
