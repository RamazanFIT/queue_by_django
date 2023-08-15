from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import News, Comment
from .forms import NewsAddModelForm
from django.views import View

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
        # title = request.POST.get("title", "")
        # content = request.POST.get("content", "")
        form = NewsAddModelForm(request.POST)
        if form.is_valid():
            news = News(title = form.cleaned_data['title'], content = form.cleaned_data["content"])
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
    return render(request, "news/main_page.html")

class NewsUpdateView(View):
    def get(self, request, news_id : int):
        news = get_object_or_404(News, pk=news_id)
        form = NewsAddModelForm(instance=news)
        return render(request, 'news/change_news.html', {'news_change_form':form, "news_id" : news_id})
    
    def post(self, request, news_id : int):
        news = get_object_or_404(News, pk=news_id)
        form = NewsAddModelForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect(reverse("news:info_news", kwargs={"news_id":news_id}))   
        return redirect(reverse("news:change_data_of_news", kwargs={"form" : form, "news_id":news_id}))     
