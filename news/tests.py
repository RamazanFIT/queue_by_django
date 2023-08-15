from django.test import TestCase
from django.urls import reverse
from .models import News, Comment
import time

class NewsHasComment(TestCase):
    def test_has_comment(self):
        a = News.objects.create(title="", content="")
        a.save()
        b = Comment(content="", news_id=a)
        b.save()
        self.assertEqual(True, a.has_comment())
    def test_has_not_comment(self):
        a = News.objects.create(title="", content="")
        a.save()
        b = News.objects.create(title="qwerty", content="roma")
        b.save()
        c = Comment(content="", news_id=b)
        c.save()
        self.assertEqual(False, a.has_comment())

class NewsAllPublishDescendingOrder(TestCase):
    def test_descending_order(self):
        a1 = News.objects.create(title="aka", content="")
        a1.save()
        time.sleep(0.001)
        a2 = News.objects.create(title="roma", content="")
        a2.save()
        time.sleep(0.001)
        a3 = News.objects.create(title="rustem", content="")
        a3.save()
        time.sleep(0.001)
        a4 = News.objects.create(title="zhirik", content="")
        a4.save()
        time.sleep(0.001)
        a5 = News.objects.create(title="timofei", content="")
        a5.save()
        
        some_list = [a1, a2, a3, a4, a5]
        response = self.client.get(reverse("news:all_news"))
        self.assertQuerysetEqual(reversed(some_list), response.context["news"])

class DetailAboutNews(TestCase):
    def test_Detail(self):
        a = News.objects.create(title="aka", content="roma")
        a.save()
        b = Comment(content="cont", news_id=a)
        b.save()
        response = self.client.get(reverse("news:info_news", kwargs={"news_id" : a.id})).context
        self.assertEqual("aka", response["news"].title)
        self.assertEqual("roma", response["news"].content)
        self.assertQuerysetEqual([b], response["comments"])

class DetailAboutNewsComment(TestCase):
    def test_DetailComment(self):
        a = News.objects.create(title="aka", content="roma")
        a.save()
        b1 = Comment(content="a", news_id=a)
        b1.save()
        time.sleep(0.001)
        b2 = Comment(content="b", news_id=a)
        b2.save()
        time.sleep(0.001)
        b3 = Comment(content="c", news_id=a)
        b3.save()
        time.sleep(0.001)
        b4 = Comment(content="d", news_id=a)
        b4.save()
        time.sleep(0.001)
        b5 = Comment(content="e", news_id=a)
        b5.save()
        time.sleep(0.001)
        b6 = Comment(content="f", news_id=a)
        b6.save()
        time.sleep(0.001)
        b7 = Comment(content="g", news_id=a)
        b7.save()

        response = self.client.get(reverse("news:info_news", kwargs={"news_id" : a.id})).context
        self.assertQuerysetEqual([b7, b6, b5, b4, b3, b2, b1], response["comments"])



