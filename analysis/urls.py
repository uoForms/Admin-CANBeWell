from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='analysis-home'),
    path('analysis/', views.data, name='analysis-data'),
    path('download/', views.Download_csv, name='analysis-csv-download'),
]
