from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class dateRangeForm(forms.Form):
    startDate = forms.DateField(widget=DateInput, label='Start Date')
    endDate = forms.DateField(widget=DateInput, label='End Date')