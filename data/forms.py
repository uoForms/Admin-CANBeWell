from django import forms

DATABASE_CHOICES= [
    ('CANBeWell_uOttawa', 'CANBeWell uOttawa'),
    ('Export_CSV_CANBeWell', 'Export CSV CANBeWell'),
    ]

class dateRangeForm(forms.Form):
    start_date = forms.CharField(label="Start Date", max_length=100)
    end_date = forms.CharField(label="End Date", max_length=100)
    db_choice = forms.CharField(label='Select Database', widget=forms.Select(choices=DATABASE_CHOICES))