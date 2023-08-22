from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout
from .forms import SignUpForm
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from rest_framework.status import HTTP_200_OK
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser

def main_page(request):
    users = CustomUser.objects.filter(is_superuser=0).order_by("created_at").all()
    enumerated_users = enumerate(users)
    return render(
        request, 
        "news/main_page.html",
        {
            "users" : enumerated_users
        }
    )




def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name="default")
            group.user_set.add(user)
            login(request, user)
            return redirect(reverse("news:main"))

    elif request.method == "GET":
        form = SignUpForm()
        return render(
            request,
            "registration/sign_up.html",
            {
                "form" : form
            }
        )
    
    return render(request, "registration/sign_up.html", {"form": form})

def log_out(request):
    logout(request)
    return redirect("/login/")
    
@login_required(login_url="/login/")
def get_profile(request):
    return render(
        request,
        "news/info_user.html"
    )

def queue(request):
    users = User.objects.all()
    users_with_index = []
    for i in range(len(users)):
        users_with_index.append()

@permission_required("user.delete_user", login_url="/news/sign_up/")
@login_required(login_url="/login/")
def admin_interface(request):
    user = CustomUser.objects.filter(is_superuser=0).order_by("created_at").first()
    return render(
        request,
        "news/organizator.html",
        {
            "user" : user
        }
    )

@permission_required("user.delete_user", login_url="/news/sign_up/")
@login_required(login_url="/login/")
def delete_user(request, user_id : int):
    user = CustomUser.objects.get(pk=user_id)
    if user is not None:
        user.delete()
    return redirect(reverse("news:admin_interface"))