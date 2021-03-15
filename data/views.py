import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.utils.safestring import mark_safe
from firebase import firebase
import pandas as pd

from data.forms import dateRangeForm

def home(request):
    context = {
        'page_title': 'Home',
     }
    return render(request, 'data/index.html', context)


def generate_date_list(start_date, end_date):
    diff = end_date - start_date
    date_list = list()
    for i in range(diff.days + 1):
        date_temp = start_date + datetime.timedelta(i)
        date_temp = date_temp.strftime("%Y%m%d")
        date_list.append(date_temp)
    return date_list


def fb_fetch_data(date_list, db_choice):
    fb_data = pd.DataFrame()
    if db_choice == "CANBeWell_uOttawa":
        fb_app_obj = firebase.FirebaseApplication("https://canbewell-uottawa.firebaseio.com/", None)
    elif db_choice == "Export_CSV_CANBeWell":
        fb_app_obj = firebase.FirebaseApplication("https://export-csv-canbewell.firebaseio.com/", None)
    fb_data_temp = fb_app_obj.get("", "")
    for i in range(0, len(date_list)):
        try:
            temp = pd.DataFrame.from_dict(fb_data_temp[date_list[i]], orient='index')
            fb_data = fb_data.append(temp)
        except:
            pass
    return fb_data

def clean_data(fb_data):
    avg_view_time = fb_data['pageviewtime'].mean()
    fb_data['pageviewtime'].fillna(avg_view_time, inplace=True)
    agerange = [''] * len(fb_data)
    for i in range(0, len(fb_data)):
        if fb_data.age[i] == 'all ages':
            agerange[i] = 'all ages'
        elif '{:0>3}'.format(fb_data.age[i]) <= '049':
            agerange[i] = 'Young'
        elif '{:0>3}'.format(fb_data.age[i]) <= '064':
            agerange[i] = 'Middle'
        else:
            agerange[i] = 'Senior'
    fb_data.insert(0, 'Firebase JSON Index', fb_data.index)
    fb_data.insert(1, 'Age Range', agerange)
    fb_data.reset_index(drop=True, inplace=True)
    fb_data.index = fb_data.index + 1
    fb_data['date'] = pd.to_datetime(fb_data['date'], format='%Y%m%d')
    fb_data['date'] = fb_data['date'].dt.strftime('%Y-%m-%d')
    return fb_data

def clean_headers(fb_data):
    fb_data.rename(columns={'age': 'Age',
                            'browser': 'Browser',
                            'city': 'City',
                            'date': 'Date',
                            'device': 'Device',
                            'gender': 'Gender',
                            'item': 'Item',
                            'language': 'Language',
                            'navigation': 'Navigation',
                            'os': 'OS',
                            'pageviewtime': 'Page View Time',
                            'region': 'Region',
                            'role': 'Role',
                            'sessionid': 'Session ID',
                            'userid': 'User ID',
                            'user': 'User'}, inplace=True)
    return fb_data

@login_required(login_url='login')
def download_csv(self):
    global fb_data
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=canbewell_data_export.csv'
    fb_data.to_csv(path_or_buf=response, index=True)
    return response


start_date = "yyyy-mm-dd"
end_date = "yyyy-mm-dd"
selected_database = "CANBeWell_uOttawa"
fb_data = pd.DataFrame()

@login_required(login_url='login')
def data(request):
    global start_date
    global end_date
    global selected_database
    global fb_data

    if request.method == 'POST':
        form = dateRangeForm(request.POST)
        if form.is_valid():
            fb_data = pd.DataFrame()
            start_date = form.cleaned_data['start_date']
            start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = form.cleaned_data['end_date']
            end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            db_choice = form.cleaned_data['db_choice']
            selected_database = db_choice
            date_list = generate_date_list(start_date_obj, end_date_obj)
            if date_list:
                fb_data = fb_fetch_data(date_list, db_choice)
                if not fb_data.empty:
                    fb_data = clean_data(fb_data)
                    fb_data = clean_headers(fb_data)
                else:
                    messages.error(request, mark_safe("No data available."))
            else:
                messages.error(request, mark_safe("Invalid dates selected."))
    else:
        form = dateRangeForm()

    context = {
        'page_title': 'Data',
        'form': form,
        'start_date': start_date,
        'end_date': end_date,
        'selected_database': selected_database,
        'fb_data': fb_data
    }

    return render(request, 'data/data.html', context)
