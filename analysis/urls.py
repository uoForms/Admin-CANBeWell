from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='analysis-home'),
    path('about/', views.about, name='analysis-about'),
    path('download/', views.Download_csv, name='analysis-csv-download'),
]
