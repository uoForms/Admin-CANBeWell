from django.urls import include, path
from . import views

urlpatterns = [
  path('', include('linkchecker.urls')),
  path('', views.button),
  path('output', views.output,name="script"),
]
