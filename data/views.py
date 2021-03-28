import datetime

import firebase_admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.utils.safestring import mark_safe
from firebase import firebase
import pandas as pd
from firebase_admin import credentials, db

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

production_ref = None
transgender_ref = None
test_ref = None
bharath_test_ref = None

def connections():
    global production_ref
    production_cred = credentials.Certificate("data/production_key.json")
    production_app = firebase_admin.initialize_app(production_cred, {
        'databaseURL': 'https://canbewell-uottawa.firebaseio.com/'
    }, name='production')
    production_ref = db.reference(app=production_app)
    global transgender_ref
    transgender_cred = credentials.Certificate("data/transgender_key.json")
    transgender_app = firebase_admin.initialize_app(transgender_cred, {
        'databaseURL': 'https://transgender-canbewell-default-rtdb.firebaseio.com/'
    }, name='transgender')
    transgender_ref = db.reference(app=transgender_app)
    global test_ref
    test_cred = credentials.Certificate("data/test_key.json")
    test_app = firebase_admin.initialize_app(test_cred, {
        'databaseURL': 'https://export-csv-canbewell.firebaseio.com/'
    }, name="test")
    test_ref = db.reference(app=test_app)
    global bharath_test_ref
    bharath_test_cred = credentials.Certificate("data/bharath_test_key.json")
    bharath_test_app = firebase_admin.initialize_app(bharath_test_cred, {
        'databaseURL': 'https://bharath-test-fe4b7-default-rtdb.firebaseio.com/'
    }, name='bharath_test')
    bharath_test_ref = db.reference(app=bharath_test_app)

def fb_fetch_data(date_list, ref):
    fb_data = pd.DataFrame()
    fb_data_temp = ref.get("", "")
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
selected_database = "Production"
fb_data = pd.DataFrame()

@login_required(login_url='login')
def data(request):
    global start_date
    global end_date
    global selected_database
    global fb_data
    global production_ref
    global transgender_ref
    global test_ref
    global bharath_test_ref

    if not production_ref or not transgender_ref or not test_ref or not bharath_test_ref:
        connections()

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
                if db_choice == "Production":
                    ref = production_ref
                elif db_choice == "Transgender":
                    ref = transgender_ref
                elif db_choice == "Test":
                    ref = test_ref
                elif db_choice == "Bharath_test":
                    ref = bharath_test_ref
                fb_data = fb_fetch_data(date_list, ref)
                if not fb_data.empty:
                    fb_data = clean_data(fb_data)
                    fb_data = clean_headers(fb_data)
                else:
                    messages.error(request, mark_safe("No data available."))
            else:
                messages.error(request, mark_safe("Invalid dates selected."))
    else:
        form = dateRangeForm()

    col_count = len(fb_data.columns) +1
    context = {
        'page_title': 'Data',
        'form': form,
        'start_date': start_date,
        'end_date': end_date,
        'selected_database': selected_database,
        'fb_data': fb_data,
        'col_count': col_count
    }

    return render(request, 'data/data.html', context)
