from django.urls import include, path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.linkchecker, name='link-checker'),
    path('output/', views.output, name='output'),
    url('^output/(?P<fileKey>.+)/(?P<idx>\d+)$', views.output_item),
    url('^output/(?P<fileKey>.+)$', views.output),
]
