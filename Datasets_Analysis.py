import pyrebase
import json
import pandas as pd
import csv
from collections import Counter
from matplotlib import pyplot as plt
from tabulate import tabulate
from prettytable import PrettyTable
import seaborn as sns
import matplotlib
import requests
import io

# Connecting to firebase database
def readfile_firebase():
    firebaseConfig = {
        'apiKey': "AIzaSyAPuIZi-ns_KRkpTjpnEbTnnAYGflqwbwI",
        'authDomain': "canbewell-uottawa.firebaseapp.com",
        'databaseURL': "https://canbewell-uottawa.firebaseio.com",
        'projectId': "canbewell-uottawa",
        'storageBucket': "canbewell-uottawa.appspot.com",
        'messagingSenderId': "813615648464",
        'appId': "1:813615648464:web:14052cf90420114be318d5",
        'measurementId': "G-935F1NQDM2"
    }

    firebase = pyrebase.initialize_app(firebaseConfig)

    return firebase.database()

# Looping through the data tree
def read_all_tree():
    all_users = readfile_firebase().child('canbewell-uottawa').get()
    for user in all_users.each():
        print(user.key())
        print(user.val())

#Looping through the child nodes
def read_child_nodes():
    data = readfile_firebase().child(20200306).get()
    records = [line.val() for line in data.each()]

    return records

    # for line in data.each():
    #     print(line.val())
#Loading data into Pandas DataFrame
def firebase_dataa_into_pandas():
    frame = pd.DataFrame(read_child_nodes())

    return frame

# print(firebase_dataa_into_pandas().head())



### Looping through the whole data tree is returning errors, thus opting for csvfile type

###Loading csv_file into DataFrame

url_original = 'https://drive.google.com/file/d/1y93LMXvqSQF7mvgO4JlOIUZ1PsiyIa-z/view?usp=sharing'
file_read = url_original.split('/')[-2]
url = 'https://drive.google.com/uc?export=download&id=' + file_read

response = requests.get(url).content
rawData = pd.read_csv(io.StringIO(response.decode('UTF-8')))
# rawData = pd.read_csv('/Users/nimat/Desktop/FinalProject/Data.csv')
print(rawData.head(4))

##Setting display
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 10)

#Quick stat display
# print(rawData.info())
# print(rawData.describe(include=['object']))
# print(rawData.shape)


##Data Cleaning

##convert the int date type to python datetime object
def convert_date():
    rawData['date'] = pd.to_datetime(rawData['date'], format='%Y%m%d')
    rawData['age'] = pd.to_numeric(rawData.age, errors = 'coerce').astype('Int64')
    return rawData['date'], rawData['age']

convert_date()

##checking the uniqueness
rawData['item'].unique()

def cleaning_data():
    rawData['item'] = rawData['item'].replace({'Covid-19': 'COVID-19', 'Lungs': 'Lung', 'Falls in the elderly':'Falls',
                                'Physical activity':'Be active', 'Covid':'COVID-19', 'PRÉVENEZ LE  COVID-19':'COVID-19', 'PRÉVENEZ LA COVID-19':'COVID-19','Memory problems  or dementia'
                                :'Memory Problems', 'lung':'Lung','Vaccination':'Immunization', 'Immunzation': 'Immunization', "Aorta:the body's main blood vessel":'Aorta', 'Liver or Alcohol/Drugs':'Liver'})

cleaning_data()
frame = rawData[rawData.gender.notnull()]
def gender_distribution(frame):
    genders = frame.gender

    gender_counter = Counter()
    gender_counter.update(genders)
    total_gender = sum(gender_counter.values())
    label, values = zip(*gender_counter.items())
    table = {}
    for gender, value in gender_counter.most_common(4):
        gender_pct = (value/total_gender)*100
        gender_pct = round(gender_pct,2)
        table[gender] = gender_pct
    print(tabulate(table.items(), headers=['Gender','Percentage(%)'], tablefmt='pretty' ))


    plt.style.use("ggplot")

    explode = [0,0.1,0,0]
    plt.pie(values, labels=label, explode=explode, shadow=True, startangle=45, autopct='%1.1f%%', wedgeprops={'edgecolor':'black'})

    plt.title('Gender distribution')
    plt.tight_layout()
    plt.show()


# gender_distribution(frame)



def Median_category():
    frame['DayOfWeek'] = frame['date'].dt.day_name()
    frame.set_index('date', inplace=True)
    computation = frame.resample('M').agg({'age':'median', 'pageviewtime':'mean'})
    print(tabulate(computation, headers=['date','age','pageviewtime'], tablefmt='pretty'))
    computation['age'].plot()
    plt.ylabel('Median Age per month')
    plt.show()
    computation['pageviewtime'].plot()
    plt.ylabel('Mean Page Viewed time')
    plt.show()

print(Median_category())

bodypart = rawData[rawData.item.notnull()]
def Most_Popular_Topics(bodypart):
    items = bodypart.item
    body_counter = Counter()
    body_counter.update(items)
    total_bodypart = sum(body_counter.values())

    topics_visited = []
    frequency  = []
    table = {}
    for item, value in body_counter.most_common(10):
        topics_visited.append(item)
        frequency.append(value)
        bodypart_pct = (value/total_bodypart)*100
        bodypart_pct = round(bodypart_pct,2)
        table[item] = bodypart_pct
    print(tabulate(table.items(), headers=['Items','Percentage(%)'], tablefmt='pretty' ))

    topics_visited.reverse()
    frequency.reverse()

    plt.barh(topics_visited,frequency)
    plt.title('Most Popular Topics')
    plt.xlabel('Frequency of visit')
    plt.tight_layout()
    plt.show()

# Most_Popular_Topics(bodypart)


def Gender_distribution_language():
    french_speaker = frame.query("language =='french'")
    english_speaker = frame.query("language =='english'")

    french_genders = french_speaker.gender
    english_gender = english_speaker.gender
    french_gender_counter = Counter()

    french_gender_counter.update(french_genders)

    total_french_gender = sum(french_gender_counter.values())

    french_labels, french_values = zip(*french_gender_counter.items())

    # print('French \n')
    table1 = {}
    for gender, value in french_gender_counter.most_common(4):

        french_gender_pct = (value / total_french_gender)*100
        french_gender_pct = round(french_gender_pct,2)
        table1[gender] = french_gender_pct


    print(tabulate(table1.items(), headers=['French_Gender','Percentage(%)'], tablefmt='pretty' ))


        # print(f'{gender}: {french_gender_pct}%')

    english_gender_counter = Counter()

    english_gender_counter.update(english_gender)

    total_english_gender = sum(english_gender_counter.values())

    english_labels, english_values = zip(*english_gender_counter.items())

    # print()

    # print('English \n')
    table2 = {}
    for gender, value in english_gender_counter.most_common(4):

        english_gender_pct = (value / total_english_gender)*100
        english_gender_pct = round(english_gender_pct,2)
        table2[gender] = english_gender_pct


    print(tabulate(table2.items(), headers=['English_Gender','Percentage(%)'], tablefmt='pretty' ))
        # print(f'{gender}: {english_gender_pct}%')

    plt.style.use("fivethirtyeight")
    explode =[0,0.1,0,0]
    plt.pie(french_values, labels=french_labels,explode=explode, shadow=True, startangle=45, autopct='%1.1f%%',wedgeprops={'edgecolor': 'black'})
    plt.title('French speakers gender distribution')
    plt.tight_layout()
    plt.show()

    print()

    plt.style.use("fivethirtyeight")
    explode =[0,0.1,0,0]
    plt.pie(english_values, labels=english_labels,explode=explode, shadow=True, startangle=45, autopct='%1.1f%%',wedgeprops={'edgecolor': 'black'})
    plt.title('English speakers gender distribution')
    plt.tight_layout()
    plt.show()

# Gender_distribution_language()

def Visual_Gender_Bar(frame):
    language_gender = frame.groupby(['language','gender'])
    agg_gender = language_gender.size().unstack()
    agg_gender_subset = agg_gender.stack()
    agg_gender_subset.name = 'total'

    agg_gender_subset = agg_gender_subset.reset_index()

    gender_language = sns.barplot(x='gender' , y= 'total', hue='language', data=agg_gender_subset)

    gender_language.set_ylabel('Frequency')
    gender_language.set_xlabel('Gender distribution')

    plt.show()

    # matplotlib.pyplot.show('hold')


# print(Visual_Gender_Bar(frame))


def Most_Viewed_topics():
    cframe = frame.pivot_table('pageviewtime', index='item', columns='agerange', aggfunc='mean')
    cframe_update = cframe.fillna(0)
    view_by_title = frame.groupby('item').size()
    activities = view_by_title.index[view_by_title >= 100]
    mean_view_time = cframe_update.loc[activities]
    viewtime_std_by_title = frame.groupby('item')['pageviewtime'].mean()
    viewtime_std_by_title= viewtime_std_by_title.loc[activities]
    most_viewed = viewtime_std_by_title.sort_values(ascending=False)[:10]

    subset = most_viewed

    ax  = sns.barplot(y=subset.index, x=subset.values)

    ax.set_ylabel('Most viewed topics')
    ax.set_xlabel('Time spent on each topic')

    plt.show()

# Most_Viewed_topics()

def MostViewedTopic_Based_on_roles():
    provider_patient = frame.groupby(['item','role'])
    agg_counts = provider_patient.size().unstack().fillna(0)
    indexer = agg_counts.sum(1).argsort()
    count_subset = agg_counts.take(indexer[-10:])
    agg_counts.sum(1).nlargest(10)

    count_subset = count_subset.stack()
    count_subset.name = 'total'
    count_subset = count_subset.reset_index()
    count_subset = count_subset[:10]


    print(tabulate(count_subset, headers=['item','role','total'], tablefmt='pretty' ))

    provider_plot = sns.barplot(x='total', y='item', hue='role', data=count_subset)

    provider_plot.set_ylabel('Most viewed topics according to role')
    provider_plot.set_xlabel('Frequency')
    plt.show()

# MostViewedTopic_Based_on_roles()


def Common_used_devices():
    by_dev_age = frame.groupby(['agerange','device'])
    by_dev_age.size().unstack().plot(kind='barh')
    plt.ylabel('Age distribution')
    plt.xlabel('Number of devices')

    plt.show()

# Common_used_devices()


def Popular_Topics_languages():
    item_language = frame.groupby(['item','language'])
    agg_item = item_language.size().unstack().fillna(0)

    index = agg_item.sum(1).argsort()
    item_subset = agg_item.take(index[-10:])
    agg_item.sum(1).nlargest(20)


    item_subset = item_subset.stack()
    item_subset.name = 'total'
    item_subset = item_subset.reset_index()
    item_subset = item_subset.sort_values('total',ascending=False)[:20]

    print(tabulate(item_subset , headers=['item','language','total'], tablefmt='pretty' ))

    item_language = sns.barplot(x='total' , y= 'item', hue='language', data=item_subset)

    # item_language.set_ylabel('Item')
    item_language.set_xlabel('Frequency')
    # item_language.invert_yaxis()

    plt.show()

# Popular_Topics_languages()
