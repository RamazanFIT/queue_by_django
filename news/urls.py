from django.urls import path, include
from . import views

app_name = 'news'


urlpatterns = [
    path("main_page/", views.main_page, name="main"),
    path("sign_up/", views.signup, name="sign_up"),
    path("logout/", views.log_out, name="logout"),
    path("profile/", views.get_profile, name="profile"),
    path("delete/user/<int:user_id>", views.delete_user, name="delete_user"),
    path("admin_interface/", views.admin_interface, name="admin_interface"),
    path("qr_code/", views.get_qr_code, name='get_qr_code')
    
]