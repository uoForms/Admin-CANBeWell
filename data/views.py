import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from firebase import firebase
import pandas as pd

from data.forms import dateRangeForm

def home(request):
    return render(request, 'data/index.html')


def generate_date_list(start_date, end_date):
    diff = end_date - start_date
    date_list = list()
    for i in range(diff.days + 1):
        date_temp = start_date + datetime.timedelta(i)
        date_temp = date_temp.strftime("%Y%m%d")
        date_list.append(date_temp)
    return date_list


def fb_fetch_data(date_list):
    fb_data = pd.DataFrame()
    fb_app_obj = firebase.FirebaseApplication("https://canbewell-uottawa.firebaseio.com/", None)
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
    fb_data.insert(0, 'firebase_json_index', fb_data.index)
    fb_data.insert(1, 'agerange', agerange)
    fb_data.reset_index(drop=True, inplace=True)
    fb_data.index = fb_data.index + 1
    return fb_data

def download_csv(self):
    global fbdata
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=canbewell_data_export.csv'
    fbdata.to_csv(path_or_buf=response, index=True)
    return response


start_date = "yyyy-mm-dd"
end_date = "yyyy-mm-dd"
fbdata = []

def data(request):
    if request.user.is_authenticated:
        global context
        global start_date
        global end_date
        global fbdata
        context = {
            'page_title': 'Data',
            'form': dateRangeForm(),
            'start_date': start_date,
            'end_date': end_date,
            'fbdata': fbdata
        }
        if request.method == 'POST':
            form = dateRangeForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                end_date = form.cleaned_data['end_date']
                end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')
                date_list = generate_date_list(start_date_obj, end_date_obj)

                global fb_data
                if date_list:
                    fb_data = fb_fetch_data(date_list)
                    fb_data = clean_data(fb_data)
                context['form'] = form
                context['fb_data'] = fb_data
                context['start_date'] = start_date
                context['end_date'] = end_date
        else:
            form = dateRangeForm()
            context['form'] = form
        return render(request, 'data/data.html', context)
    else:
        return redirect('home_page')
