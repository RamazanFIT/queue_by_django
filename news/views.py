from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout
from .models import News, Comment
from .forms import NewsAddModelForm, SignUpForm
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from rest_framework.status import HTTP_200_OK
from .serializers import NewsModelSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

def get_info_about_new(request, news_id : int):
    if request.method == "GET":
        news = get_object_or_404(News, pk=news_id)
        comments = Comment.objects.order_by("-created_at").filter(news_id_id = news_id).all()
        return render(request, "news/info_news.html", {"news" : news, "comments" : comments})
    elif request.method == "POST" and request.user.is_authenticated or request.user.has_perm("news.add_comment"):
        user = get_object_or_404(User,pk=request.user.id)
        news = get_object_or_404(News, pk=news_id)
        content = request.POST.get("content", "")
        comment = Comment(content=content, news_id=news, author_of_comment=user)
        comment.save()
        return redirect(reverse("news:info_news", kwargs={"news_id" : news_id}))

@permission_required("news.add_news", login_url="/login")
@login_required(login_url="/login/")
def add_news(request):
    if request.method == "POST":
        # title = request.POST.get("title", "")
        # content = request.POST.get("content", "")
        form = NewsAddModelForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User,pk=request.user.id)
            news = News(title = form.cleaned_data['title'], content = form.cleaned_data["content"], author_of_news=user)
            news.save()
            return redirect(reverse("news:info_news", kwargs={"news_id": news.id}))
        else:
            return redirect(reverse("news:interface_adding", {"news_add_form" : form}))
    elif request.method == "GET":
        news_add_form = NewsAddModelForm()
        return render(request, "news/add_news.html", {"news_add_form" : news_add_form})
     
def get_all_news(request):
    news = News.objects.order_by("-created_at").all()
    return render(request, "news/get_all_news.html", {"news" : news})

def main_page(request):
    return render(
        request, 
        "news/main_page.html",
    )


class NewsUpdateView(View):
    # @method_decorator(permission_required("news.change_news", login_url="/login"))
    def get(self, request, news_id : int):
        news = get_object_or_404(News, pk=news_id)
        if request.user == news.author_of_news or request.user.has_perm("news.change_news"): 
            form = NewsAddModelForm(instance=news)
            return render(request, 'news/change_news.html', {'news_change_form':form, "news_id" : news_id})
        return HttpResponse("Permission denied")

    # @method_decorator(permission_required("news.change_news", login_url="/login"))
    def post(self, request, news_id : int):
        news = get_object_or_404(News, pk=news_id)
        if request.user == news.author_of_news or request.user.has_perm("news.change_news"):
            form = NewsAddModelForm(request.POST, instance=news)
            if form.is_valid():
                form.save()
                return redirect(reverse("news:info_news", kwargs={"news_id":news_id}))   
            return redirect(reverse("news:change_data_of_news", kwargs={"form" : form, "news_id":news_id}))     
        else:
            return HttpResponseRedirect("/error", {"message" : "Error"})


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
    else:
        return redirect(reverse("news:main"))

def log_out(request):
    logout(request)
    return redirect("/login/")
    
@login_required(login_url="/login/")
def get_profile(request):
    return render(
        request,
        "news/info_user.html"
    )

def comment_delete(request, comment_id : int, news_id : int):
    comment = get_object_or_404(Comment, pk=comment_id)
    news = get_object_or_404(News, pk=news_id)
    if comment.author_of_comment == request.user or request.user.has_perm("news.delete_comment") or news.author_of_news == request.user:
        comment.delete()
    return redirect(reverse("news:info_news", kwargs={"news_id" : news_id}))


def delete_news(request, news_id : int, user_id : int):
    news = get_object_or_404(News, pk=news_id)
    if news.author_of_news == request.user or request.user.has_perm("news.delete_news"):
        news.delete()
    return redirect(reverse("news:all_news"))

class NewsAddView(
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = News.objects.all()
    serializer_class = NewsModelSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



@api_view(["GET"])
def get_news(request):
    news = get_list_or_404(News)
    serializer = NewsModelSerializer(news, many=True)
    return Response(serializer.data)

class NewsGetDeleteView(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView
):
    queryset = News.objects.all()
    serializer_class = NewsModelSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)