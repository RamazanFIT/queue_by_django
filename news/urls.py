from django.urls import path, include
from . import views

app_name = 'news'


urlpatterns = [
    path("<int:news_id>/", views.get_info_about_new, name="info_news"),
    path("add_news/", views.add_news, name="interface_adding"),
    path("", views.get_all_news, name="all_news"),
    path("main_page", views.main_page, name="main")
]