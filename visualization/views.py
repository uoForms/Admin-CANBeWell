from django.shortcuts import render

from visualization.Datasets_Analysis import *

def visualization(request):
    
    dataset = DatasetAnalysis()
    ## dataset.run()
    gender_distribution_uri, gender_distribution_table = dataset.gender_distribution()
    # median_category_uri, median_category_table = dataset.Median_category()
    Median_Age = dataset.Median_Age()
    # most_popular_topics_uri, most_popular_topics_table = dataset.Most_Popular_Topics()
    french_gender_dis_uri, french_gender_dis_table, english_gender_dis_uri, english_gender_dis_table = dataset.Gender_distribution_language()
    visual_gender_bar_uri = dataset.Visual_Gender_Bar()
    # most_viewed_topics_uri = dataset.Most_Viewed_topics()
    mostviewedtopic_based_on_roles_uri, mostviewedtopic_based_on_roles_table = dataset.MostViewedTopic_Based_on_roles()
    common_used_devices_uri = dataset.Common_used_devices()
    ItemsGenderSpecific_uri = dataset.ItemsGenderSpecific()
    popular_topics_languages_uri, popular_topics_languages_table = dataset.Popular_Topics_languages()
    # Topic_Distribution_uri = dataset.Topic_Distribution()

    fig_data = {
         'page_title': 'Visualization',
         'gender_distribution_uri': gender_distribution_uri,
         "gender_distribution_table": gender_distribution_table,
    #     'median_category_uri': median_category_uri,
    #     'median_category_table': median_category_table,
    #     "most_popular_topics_uri": most_popular_topics_uri,
    #     "most_popular_topics_table": most_popular_topics_table,
         "french_gender_dis_uri": french_gender_dis_uri,
         "french_gender_dis_table": french_gender_dis_table,
         "english_gender_dis_uri": english_gender_dis_uri,
         "english_gender_dis_table": english_gender_dis_table,
         "visual_gender_bar_uri": visual_gender_bar_uri,
    #     'most_viewed_topics_uri': most_viewed_topics_uri,
         'mostviewedtopic_based_on_roles_uri': mostviewedtopic_based_on_roles_uri,
         'mostviewedtopic_based_on_roles_table': mostviewedtopic_based_on_roles_table,
         'common_used_devices_uri': common_used_devices_uri,
         'popular_topics_languages_uri': popular_topics_languages_uri,
         'popular_topics_languages_table': popular_topics_languages_table,
         'ItemsGenderSpecific_uri': ItemsGenderSpecific_uri,
    #     'Topic_Distribution_uri': Topic_Distribution_uri,
          'Median_Age': Median_Age
    }

    return render(request, "visualization/index.html", fig_data)
