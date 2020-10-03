from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='analysis-home'),
    path('about/', views.about, name='analysis-about'),
    path('viz/', views.viz, name='analysis-viz'),
    path('download/', views.Download_csv, name='analysis-csv-download'),
]
