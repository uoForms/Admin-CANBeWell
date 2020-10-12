from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from firebase import firebase
import pandas as pd
import datetime
import pyrebase
import dash_core_components as dcc
import dash_html_components as html
import dash_table


# Create your views here.


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



def visual(request):
    return render(request, "visualPage/visual.html")