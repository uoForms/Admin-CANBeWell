from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.utils.safestring import mark_safe
from visualization.Datasets_Analysis import *
from data import views

dataset = None
gender_distribution_uri = None
most_popular_topics_uri = None
french_gender_dis_uri = None
english_gender_dis_uri = None
visual_gender_bar_uri = None
mostviewedtopic_based_on_roles_uri = None
common_used_devices_uri = None
popular_topics_languages_uri = None
ItemsGenderSpecific_uri = None
Topic_Distribution_uri = None
Median_Age = None
start_date = "yyyy-mm-dd"
end_date = "yyyy-mm-dd"

@login_required(login_url='/')
def visualization(request):
    global dataset
    global start_date
    global end_date
    global gender_distribution_uri
    global most_popular_topics_uri
    global french_gender_dis_uri
    global english_gender_dis_uri
    global visual_gender_bar_uri
    global mostviewedtopic_based_on_roles_uri
    global common_used_devices_uri
    global popular_topics_languages_uri
    global ItemsGenderSpecific_uri
    global Topic_Distribution_uri
    global Median_Age
    if request.method == 'POST':
        start_date = views.start_date
        end_date = views.end_date
        fb_data = views.fb_data
        if not fb_data.empty:
            dataset = DatasetAnalysis(fb_data)
            gender_distribution_uri, gender_distribution_table = dataset.gender_distribution()
            # median_category_uri, median_category_table = dataset.Median_category()
            Median_Age = dataset.Median_Age()
            most_popular_topics_uri, most_popular_topics_table = dataset.Most_Popular_Topics()
            french_gender_dis_uri, french_gender_dis_table, english_gender_dis_uri, english_gender_dis_table = dataset.Gender_distribution_language()
            visual_gender_bar_uri = dataset.Visual_Gender_Bar()
            # most_viewed_topics_uri = dataset.Most_Viewed_topics()
            mostviewedtopic_based_on_roles_uri, mostviewedtopic_based_on_roles_table = dataset.MostViewedTopic_Based_on_roles()
            common_used_devices_uri = dataset.Common_used_devices()
            ItemsGenderSpecific_uri = dataset.ItemsGenderSpecific()
            popular_topics_languages_uri, popular_topics_languages_table = dataset.Popular_Topics_languages()
            Topic_Distribution_uri = dataset.Topic_Distribution()
        else:
            messages.error(request, mark_safe("No data available to generate charts."))

    fig_data = {
        'page_title': 'Visualization',
        'start_date': start_date,
        'end_date': end_date,
        'gender_distribution_uri': gender_distribution_uri,
        # 'median_category_uri': median_category_uri,
        # 'median_category_table': median_category_table,
        "most_popular_topics_uri": most_popular_topics_uri,
        "french_gender_dis_uri": french_gender_dis_uri,
        "english_gender_dis_uri": english_gender_dis_uri,
        "visual_gender_bar_uri": visual_gender_bar_uri,
        # 'most_viewed_topics_uri': most_viewed_topics_uri,
        'mostviewedtopic_based_on_roles_uri': mostviewedtopic_based_on_roles_uri,
        'common_used_devices_uri': common_used_devices_uri,
        'popular_topics_languages_uri': popular_topics_languages_uri,
        'ItemsGenderSpecific_uri': ItemsGenderSpecific_uri,
        'Topic_Distribution_uri': Topic_Distribution_uri,
        'Median_Age': Median_Age
    }
    if start_date == "yyyy-mm-dd":
        print(start_date)
    return render(request, "visualization/index.html", fig_data)
