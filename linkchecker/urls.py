from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.linkchecker, name='link-checker'),
    path('output/', views.output, name="output")
]
