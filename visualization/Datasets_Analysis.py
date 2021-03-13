import pyrebase
import json
import pandas as pd
import csv
from collections import Counter
from matplotlib import pyplot as plt, figure
from tabulate import tabulate
import seaborn as sns
import requests
import io
import mpld3
import urllib
import base64

class DatasetAnalysis():

    def __init__(self, fb_data):
        self.initrawData(fb_data)
        self.convert_date()
        self.rawData['item'].unique()
        self.cleaning_data()
        self.frame = self.rawData[self.rawData.gender.notnull()]
        self.bodypart = self.rawData[self.rawData.item.notnull()]

    def initrawData(self,fb_data):
        self.rawData = pd.DataFrame(fb_data)
        self.rawData['gender'] = self.rawData['gender'].str.capitalize()
        self.rawData.rename(columns={
                            'language': 'Languages', 'device': 'Device', 'role': 'Roles'}, inplace=True)

        self.rawData['Roles'] = self.rawData['Roles'].str.capitalize()
        self.rawData['Languages'] = self.rawData['Languages'].str.capitalize()

        self.rawData['agerange'] = self.rawData['agerange'].str.replace(
            'all ages', 'Unspecfied')
        pd.set_option('display.max_columns', 100)
        pd.set_option('display.max_rows', 10)

    def convert_date(self):
        self.rawData['date'] = pd.to_datetime(
            self.rawData['date'], format='%Y%m%d')
        self.rawData['age'] = pd.to_numeric(
            self.rawData.age, errors='coerce').astype('Int64')
        return self.rawData['date'], self.rawData['age']

    def cleaning_data(self):
        self.rawData['item'] = self.rawData['item'].replace({'Covid-19': 'COVID-19', 'Lungs': 'Lung', 'Falls in the elderly': 'Falls',
                                                             'Physical activity': 'Be active', 'Covid': 'COVID-19', 'PRÉVENEZ LE  COVID-19': 'COVID-19', 'PRÉVENEZ LA COVID-19': 'COVID-19', 'Memory problems  or dementia': 'Memory Problems', 'lung': 'Lung', 'Vaccination': 'Immunization', 'Immunzation': 'Immunization', "Aorta:the body's main blood vessel": 'Aorta', 'Liver or Alcohol/Drugs': 'Liver'})

    def gender_distribution(self):
        plt.clf()

        genders = self.frame.gender

        gender_counter = Counter()
        gender_counter.update(genders)
        total_gender = sum(gender_counter.values())
        label, values = zip(*gender_counter.items())
        table = {}
        for gender, value in gender_counter.most_common(4):
            gender_pct = (value / total_gender) * 100
            gender_pct = round(gender_pct, 2)
            table[gender] = gender_pct
        output_table1 = tabulate(table.items(), headers=[
                                 'Gender', 'Percentage(%)'], tablefmt='html')

        self.gender_distribution_table = output_table1
        # print("====gender_distribution====")
        # print(output_table1)
        # print("=" * 30)

        plt.style.use("ggplot")

        explode = [0, 0.1]
        plt.pie(values, labels=label, explode=explode, shadow=True,
                startangle=45, autopct='%1.1f%%', wedgeprops={'edgecolor': 'black'})

        # plt.pie(values, labels=label, shadow=True,
        #         startangle=45, autopct='%1.1f%%', wedgeprops={'edgecolor': 'black'})

        # plt.title('Gender distribution')
        plt.tight_layout()

        # plt.show()

        # self.gender_distribution_fig = plt.gcf()
        uri = self.getBase64URI(plt.gcf())

        return uri, self.gender_distribution_table

    def Topic_distribution(self):
          plt.clf()

          genders = self.frame.gender

          gender_counter = Counter()
          gender_counter.update(genders)
          total_gender = sum(gender_counter.values())
          label, values = zip(*gender_counter.items())
          table = {}
          for gender, value in gender_counter.most_common(4):
              gender_pct = (value / total_gender) * 100
              gender_pct = round(gender_pct, 2)
              table[gender] = gender_pct
          output_table1 = tabulate(table.items(), headers=[
                                   'Gender', 'Percentage(%)'], tablefmt='html')

          self.gender_distribution_table = output_table1
     #    # print("====gender_distribution====")
     #    # print(output_table1)
     #    # print("=" * 30)

          plt.style.use("ggplot")

          explode = [0, 0.1, 0, 0]
          plt.pie(values, labels=label, explode=explode, shadow=True,
                  startangle=45, autopct='%1.1f%%', wedgeprops={'edgecolor': 'black'})

     #    # plt.title('Gender distribution')
          plt.tight_layout()

     #    # plt.show()

     #    # self.gender_distribution_fig = plt.gcf()
          uri = self.getBase64URI(plt.gcf())

          return uri, self.gender_distribution_table

    def Median_category(self):
        plt.rcParams['axes.facecolor'] = 'white'
        plt.clf()
        self.frame['DayOfWeek'] = self.frame['date'].dt.day_name()
        self.frame.set_index('date', inplace=True)
        computation = self.frame.resample('M').agg(
            {'age': 'median', 'pageviewtime': 'mean'})
        output_table2 = tabulate(computation, headers=[
            'date', 'age', 'pageviewtime'], tablefmt='html')

        # print("====Median_category====")
        # print(output_table2)
        # print("=" * 30)

        self.median_category_table = output_table2

        # computation['age'].plot()
        # plt.ylabel('Median Age per month')
        # plt.savefig('Median age distribution', bbox_inches='tight')
        # plt.show()
        # computation['pageviewtime'].plot()
        computation['age'].plot()
        plt.ylabel('Median Age Distribution')
        # plt.title("Median Category")
        # plt.savefig('Mean_pageviewtime', bbox_inches='tight')
        plt.tight_layout()
        # plt.show()
        uri = self.getBase64URI(plt.gcf())

        return uri, self.median_category_table

    def Median_Age(self):
        plt.rcParams['axes.facecolor'] = 'white'
        plt.clf()
        self.frame['DayOfWeek'] = self.frame['date'].dt.day_name()
        self.frame.set_index('date', inplace=True)
        computation = self.frame.resample('M').agg({'age': 'median', 'pageviewtime': 'mean'})
        output_table2 = tabulate(computation, headers=['date', 'age', 'pageviewtime'], tablefmt='html')
        self.median_category_table = output_table2
        computation['age'].plot()
        plt.ylabel('Mediam Age Per Month')
        plt.tight_layout()
        # plt.show()
        age_dist = self.getBase64URI(plt.gcf())

        return age_dist

    def Most_Popular_Topics(self):
        plt.clf()
        items = self.bodypart.item
        body_counter = Counter()
        body_counter.update(items)
        total_bodypart = sum(body_counter.values())

        topics_visited = []
        frequency = []
        table = {}
        for item, value in body_counter.most_common(10):
            topics_visited.append(item)
            frequency.append(value)
            bodypart_pct = (value / total_bodypart) * 100
            bodypart_pct = round(bodypart_pct, 2)
            table[item] = bodypart_pct
        output_table3 = tabulate(table.items(), headers=[
            'Items', 'Percentage(%)'], tablefmt='html', )

        self.most_popular_topics_table = output_table3

        # print("====Most_Popular_Topics====")
        # print(output_table3)
        # print("=" * 30)

        topics_visited.reverse()
        frequency.reverse()
        my_colors = list('rgbkymc')
        plt.barh(topics_visited, frequency, color=my_colors)
        # plt.title('Most Popular Topics')
        plt.xlabel('Frequency of visit')
        plt.tight_layout()

        # plt.savefig('Most_Popular_Topics', bbox_inches='tight')

        # plt.show()
        uri = self.getBase64URI(plt.gcf())

        return uri, self.most_popular_topics_table

    def Topic_Distribution(self):
        plt.clf()
        items = self.bodypart.item
        body_counter = Counter()
        body_counter.update(items)
        total_bodypart = sum(body_counter.values())

        topics_visited = []
        frequency = []
        table = {}
        for item, value in body_counter.most_common(7):
            topics_visited.append(item)
            frequency.append(value)
            bodypart_pct = (value / total_bodypart) * 100
            bodypart_pct = round(bodypart_pct, 2)
            table[item] = bodypart_pct
        output_table3 = tabulate(table.items(), headers=[
            'Items', 'Percentage(%)'], tablefmt='html', )

        self.most_popular_topics_table = output_table3

        plt.style.use("fivethirtyeight")
        explode = [0, 0, 0, 0, 0, 0, 0.1]
        plt.pie(frequency, labels=topics_visited, explode=explode, shadow=True,
                startangle=45, autopct='%1.1f%%', wedgeprops={'edgecolor': 'black'})
        # plt.title('French speakers gender distribution')
        plt.tight_layout()
        # plt.show()
        uri = self.getBase64URI(plt.gcf())

        return uri

    def Gender_distribution_language(self):

        french_speaker = self.frame.query("Languages =='French'")
        english_speaker = self.frame.query("Languages =='English'")

        french_genders = french_speaker.gender
        english_gender = english_speaker.gender
        french_gender_counter = Counter()

        french_gender_counter.update(french_genders)

        total_french_gender = sum(french_gender_counter.values())

        french_labels, french_values = zip(*french_gender_counter.items())

        # print('French \n')
        table1 = {}
        for gender, value in french_gender_counter.most_common(4):

            french_gender_pct = (value / total_french_gender) * 100
            french_gender_pct = round(french_gender_pct, 2)
            table1[gender] = french_gender_pct

        output_table4 = tabulate(table1.items(), headers=[
            'French_Gender', 'Percentage(%)'], tablefmt='html')

        self.french_gender_distribution_language_table = output_table4
        # print("Fsrench_Gender_distribution_language")
        # print(output_table4)
        # print("=" * 30)

        # print(f'{gender}: {french_gender_pct}%')

        english_gender_counter = Counter()

        english_gender_counter.update(english_gender)

        total_english_gender = sum(english_gender_counter.values())

        english_labels, english_values = zip(*english_gender_counter.items())

        # print()

        # print('English \n')
        table2 = {}
        for gender, value in english_gender_counter.most_common(4):

            english_gender_pct = (value / total_english_gender) * 100
            english_gender_pct = round(english_gender_pct, 2)
            table2[gender] = english_gender_pct

        output_table5 = tabulate(table2.items(), headers=[
            'English_Gender', 'Percentage(%)'], tablefmt='html')

        self.english_gender_distribution_language_table = output_table5

        # print("English_Gender_distribution_language")
        # print(output_table5)
        # print("=" * 30)

        plt.clf()
        plt.style.use("fivethirtyeight")
        explode = [0, 0.1]
        plt.pie(french_values, labels=french_labels, explode=explode, shadow=True,
                startangle=45, autopct='%1.1f%%', wedgeprops={'edgecolor': 'black'})

        # plt.title('French speakers gender distribution')
        plt.tight_layout()

        french_gender_dis_fig = self.getBase64URI(plt.gcf())
        # plt.show()

        plt.clf()
        plt.style.use("fivethirtyeight")
        explode = [0, 0.1]
        plt.pie(english_values, labels=english_labels, explode=explode, shadow=True,
                startangle=45, autopct='%1.1f%%', wedgeprops={'edgecolor': 'black'})

        # plt.title('English speakers gender distribution')
        plt.tight_layout()
        english_gender_dis_fig = self.getBase64URI(plt.gcf())

        # plt.show()
        return french_gender_dis_fig, output_table4, english_gender_dis_fig, output_table5

    def Visual_Gender_Bar(self):
        plt.clf()
        language_gender = self.frame.groupby(['Languages', 'gender'])
        agg_gender = language_gender.size().unstack()
        agg_gender_subset = agg_gender.stack()
        agg_gender_subset.name = 'total'

        agg_gender_subset = agg_gender_subset.reset_index()

        gender_language = sns.barplot(
            x='gender', y='total', hue='Languages', data=agg_gender_subset)

        gender_language.set_ylabel('Frequency')
        gender_language.set_xlabel('Gender distribution')

        # plt.savefig('Genders_in_barcharts', bbox_inches='tight')

        # plt.title("Visual Gender Bar")
        plt.tight_layout()
        # plt.show()
        # matplotlib.pyplot.show('hold')

        uri = self.getBase64URI(plt.gcf())

        return uri

    def ItemsGenderSpecific(self):
        plt.clf()
        # language_gender = self.frame.groupby(['item', 'gender'])
        topic_gender = self.frame.groupby(['item', 'gender'])
        agg_topic = topic_gender.size().unstack()
        agg_topic_subset = agg_topic.stack()

        agg_topic_subset.name = 'total'

        agg_topic_subset = agg_topic_subset.reset_index()
        agg_topic_subset = agg_topic_subset.sort_values(
            'total', ascending=False)[:10]

        sns.color_palette("Set2")
        # sns.color_palette("husl", 8)
        # sns.set(size=6)
        gender_topic = sns.barplot(
            x='total', y='item', hue='gender', data=agg_topic_subset)
        gender_topic.legend(loc='center right')

        sns.set(style="whitegrid")
        plt.tight_layout()

        uri = self.getBase64URI(plt.gcf())

        return uri

    def Most_Viewed_topics(self):
        plt.clf()
        cframe = self.frame.pivot_table(
            'pageviewtime', index='item', columns='agerange', aggfunc='mean')
        cframe_update = cframe.fillna(0)
        view_by_title = self.frame.groupby('item').size()
        activities = view_by_title.index[view_by_title >= 100]
        mean_view_time = cframe_update.loc[activities]
        viewtime_std_by_title = self.frame.groupby(
            'item')['pageviewtime'].mean()
        viewtime_std_by_title = viewtime_std_by_title.loc[activities]
        most_viewed = viewtime_std_by_title.sort_values(ascending=False)[:10]

        subset = most_viewed
        sns.set(style="whitegrid")

        ax = sns.barplot(y=subset.index, x=subset.values)

        ax.set_ylabel('Most viewed topics')
        ax.set_xlabel('Time spent on each topic')
        # plt.title("Most Viewed Topics")

        # plt.savefig('Most_Viewed_topics', bbox_inches='tight')
        # plt.show()
        plt.tight_layout()
        uri = self.getBase64URI(plt.gcf())
        # plt.show()
        return uri

    def MostViewedTopic_Based_on_roles(self):
        plt.clf()
        provider_patient = self.frame.groupby(['item', 'Roles'])
        agg_counts = provider_patient.size().unstack().fillna(0)
        indexer = agg_counts.sum(1).argsort()
        count_subset = agg_counts.take(indexer[-10:])
        agg_counts.sum(1).nlargest(10)

        count_subset = count_subset.stack()
        count_subset.name = 'total'
        count_subset = count_subset.reset_index()
        count_subset = count_subset[:10]

        output_table6 = tabulate(count_subset, headers=[
            'item', 'Roles', 'total'], tablefmt='html')

        # print("MostViewedTopic_Based_on_roles")
        # print(output_table6)
        self.mostviewedtopic_based_on_roles_table = output_table6
        # print("=" * 30)

        provider_plot = sns.barplot(
            x='total', y='item', hue='Roles', data=count_subset)

        provider_plot.set_ylabel('Most viewed topics according to Roles')
        provider_plot.set_xlabel('Frequency')
        # plt.savefig('MostViewedTopic_Based_on_roles', bbox_inches='tight')

        # plt.show()
        # plt.title("MostViewedTopic Based On Roles")
        plt.tight_layout()
        uri = self.getBase64URI(plt.gcf())
        return uri, self.mostviewedtopic_based_on_roles_table

    def Common_used_devices(self):

        plt.clf()
        by_dev_age = self.frame.groupby(['agerange', 'Device'])
        figure = by_dev_age.size().unstack().plot(kind='barh')
        # plt.rcParams["figure.figsize"] = (25, 5)
        plt.xlabel('Number of devices')
        plt.ylabel('Age Categories')
        # plt.savefig('Common_used_devices', bbox_inches='tight')
        # plt.show()
        # plt.title("Common Used Devices")
        plt.tight_layout()
        uri = self.getBase64URI(plt.gcf())

        return uri

        # fig = plt.figure()

        # mpld3.save_hmtl(fig, 'test.html')
        # mpld3.fig_to_html(fig, template_type='simple')
        # mpld3.disable_notebook()
        # mpld3.show()

        # fig = plt.savefig('fig')
        # html_str = mpld3.fig_to_html(fig)
        # Html_file = open("/Users/nimat/Desktop/index.html", "w")
        # Html_file.write(html_str)
        # Html_file.close()

    def Popular_Topics_languages(self):
        plt.clf()
        item_language = self.frame.groupby(['item', 'Languages'])
        agg_item = item_language.size().unstack().fillna(0)

        index = agg_item.sum(1).argsort()
        item_subset = agg_item.take(index[-10:])
        agg_item.sum(1).nlargest(20)

        item_subset = item_subset.stack()
        item_subset.name = 'total'
        item_subset = item_subset.reset_index()
        item_subset = item_subset.sort_values('total', ascending=False)[:20]

        output_table7 = tabulate(item_subset, headers=[
            'item', 'language', 'total'], tablefmt='html')

        # print("Popular_Topics_languages")
        self.popular_topics_languages_table = output_table7
        # print(output_table7)
        # print("=" * 30)

        item_language = sns.barplot(
            x='total', y='item', hue='Languages', data=item_subset)

        item_language.set_ylabel('Item')
        item_language.set_xlabel('Frequency')
        # item_language.invert_yaxis()
        # plt.title("Popular Topics Languages")
        plt.tight_layout()
        # plt.show()

        # plt.savefig('Popular_Topics_languages', bbox_inches='tight')

        uri = self.getBase64URI(plt.gcf())
        return uri, self.popular_topics_languages_table

    def getBase64URI(self, fig):
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)

        return uri
