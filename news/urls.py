from django.urls import path, include
from . import views

app_name = 'news'


urlpatterns = [
    path("<int:news_id>/", views.get_info_about_new, name="info_news"),
    path("add_news/", views.add_news, name="interface_adding"),
    path("", views.get_all_news, name="all_news"),
    path("main_page/", views.main_page, name="main"),
    path('<int:news_id>/edit/', views.NewsUpdateView.as_view(), name="change_data_of_news"),
    path("sign_up/", views.signup, name="sign_up"),
    path("logout/", views.log_out, name="logout"),
    path("profile/", views.get_profile, name="profile"),
    path("delete_comment/<int:comment_id>/<int:news_id>/", views.comment_delete, name="delete_comment"),
    path("delete_news/<int:news_id>/<int:user_id>", views.delete_news, name="delete_news"),
    path("api/news/add", views.NewsAddView.as_view(), name="news_add_view"),
    path("api/news/", views.get_news, name="get_news"),
    path("api/news/<int:pk>", views.NewsGetDeleteView.as_view(), name="get_or_delete_news")
]