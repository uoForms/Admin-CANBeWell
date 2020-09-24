from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='analysis-home'),
    path('about/', views.about, name='analysis-about'),
    path('login/', views.login, name='firebase-login'),
    path('logout/', views.logout, name='firebase-logout'),
    path('viz/', views.viz, name='analysis-viz'),
    path('download/', views.Download_csv, name='analysis-csv-download'),
]
