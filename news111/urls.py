from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'news'


urlpatterns = [
    path("some_input/", views.some_input),
    path("obr_input/", views.obr),
    path("some_output/<str:some_text>/", views.some_output, name="some")
    
]







