from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.http import Http404
from django.contrib import messages
from firebase import firebase
import pandas as pd
from .myform import dateRangeForm
from django.utils.safestring import mark_safe
import datetime
import pyrebase
import csv,io


firebaseConfig = {
    'apiKey': "AIzaSyAPuIZi-ns_KRkpTjpnEbTnnAYGflqwbwI",
    'authDomain': "canbewell-uottawa.firebaseapp.com",
    'databaseURL': "https://canbewell-uottawa.firebaseio.com",
    'projectId': "canbewell-uottawa",
    'storageBucket': "canbewell-uottawa.appspot.com",
    'messagingSenderId': "813615648464",
    'appId': "1:813615648464:web:14052cf90420114be318d5",
    'measurementId': "G-935F1NQDM2",
}
firebaseInit = pyrebase.initialize_app(firebaseConfig)
auth = firebaseInit.auth()

def home(request):
    context = {
        'page_title': 'Home'
    }
    return render(request, 'analysis/home.html', context)


def firebase_date_range(startDate, endDate):
    diff = endDate - startDate
    date_list = list()
    for i in range(diff.days + 1):
        date_temp = startDate + datetime.timedelta(i)
        date_temp = date_temp.strftime("%Y%m%d")
        date_list.append(date_temp)
    return date_list


def firebase_live_connection(date_list):
    fbdata = pd.DataFrame()
    fbobject = firebase.FirebaseApplication("https://canbewell-uottawa.firebaseio.com/", None)
    fbdata_temp = fbobject.get("", "")
    for i in range(0, len(date_list)):
        try:
            temp = pd.DataFrame.from_dict(fbdata_temp[date_list[i]], orient='index')
            fbdata = fbdata.append(temp)
        except:
            print('date exception caught -- ', str(date_list[i]))
    return fbdata


def data_cleaning(fbdata):
    avg_view_time = fbdata['pageviewtime'].mean()
    fbdata['pageviewtime'].fillna(avg_view_time, inplace=True)
    agerange = [''] * len(fbdata)
    for i in range(0, len(fbdata)):
        if fbdata.age[i] == 'all ages':
            agerange[i] = 'all ages'
        elif '{:0>3}'.format(fbdata.age[i]) <= '049':
            agerange[i] = 'Young'
        elif '{:0>3}'.format(fbdata.age[i]) <= '064':
            agerange[i] = 'Middle'
        else:
            agerange[i] = 'Senior'
    fbdata.insert(0, 'firebase_json_index', fbdata.index)
    fbdata.insert(1, 'agerange', agerange)
    fbdata.reset_index(drop=True, inplace=True)
    fbdata.index = fbdata.index + 1
    return fbdata


def Download_csv(self):
    global fbdata
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=canbewell_data_export.csv'
    fbdata.to_csv(path_or_buf=response, index=True)
    return response

start_date = "yyyy-mm-dd"
end_date = "yyyy-mm-dd"

def data(request):
    global context
    global start_date
    global end_date
    context = {
        'page_title': 'Data',
        'form': dateRangeForm(),
        'start_date': start_date,
        'end_date': end_date
    }
    if request.method == 'POST':
        request_name = request.POST.get('name')
        print(request_name)
        if request_name == 'login_form':
            try:
                email = request.POST.get('email')
                password = request.POST.get('password')
                firebaseUser = auth.sign_in_with_email_and_password(email, password)
                print(firebaseUser)
                validation = 1
                context = {
                    'page_title': 'Firebase Data',
                    'form': dateRangeForm(),
                    'validation': validation,
                    'email': email,
                    'password': password,
                    'firebaseUser': firebaseUser
                }
            except:
                context['validation'] = 0
            return render(request, 'analysis/data.html', context)


        elif request_name == 'connection_form':
            form = dateRangeForm(request.POST)
            if form.is_valid():
                try:
                    start_date = form.cleaned_data['start_date']
                    start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                    end_date = form.cleaned_data['end_date']
                    end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')
                    date_list = firebase_date_range(start_date_obj, end_date_obj)
                    if date_list:
                        global fbdata
                        fbdata = firebase_live_connection(date_list)
                        fbdata = data_cleaning(fbdata)
                        context['fbdata'] = fbdata
                        context['start_date'] = start_date
                        context['end_date'] = end_date
                except:
                    messages.error(request, mark_safe("Invalid dates.<br/> No data available"))
            return render(request, 'analysis/data.html', context)

    return render(request, 'analysis/data.html', context)

