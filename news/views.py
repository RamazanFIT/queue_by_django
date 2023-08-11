from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import News, Comment


def get_info_about_new(request, news_id : int):
    if request.method == "GET":
        news = get_object_or_404(News, pk=news_id)
        comments = Comment.objects.order_by("-created_at").filter(news_id_id = news_id).all()
        return render(request, "news/info_news.html", {"news" : news, "comments" : comments})
    elif request.method == "POST":
        news = get_object_or_404(News, pk=news_id)
        content = request.POST.get("content", "")
        comment = Comment(content=content, news_id=news)
        comment.save()
        return redirect(reverse("news:info_news", kwargs={"news_id" : news_id}))

def add_news(request):
    if request.method == "POST":
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        news = News(title = title, content = content)
        news.save()
        return redirect(reverse("news:info_news", kwargs={"news_id": news.id}))
    elif request.method == "GET":
        return render(request, "news/add_news.html")
    
    
def get_all_news(request):
    news = News.objects.order_by("-created_at").all()
    return render(request, "news/get_all_news.html", {"news" : news})

def main_page(request):
    return render(request, "news/main_page.html")

