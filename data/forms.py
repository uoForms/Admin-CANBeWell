from django import forms


class dateRangeForm(forms.Form):
    start_date = forms.CharField(label="start_date", max_length=100)
    end_date = forms.CharField(label="end_date", max_length=100)