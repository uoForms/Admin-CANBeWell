from django.urls import path
from . import views


urlpatterns = [
    path("", views.visual, name="visual")
]