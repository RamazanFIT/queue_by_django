from django.db import models
from django.contrib.auth.models import User

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    author_of_news = models.ForeignKey(User, on_delete=models.CASCADE)


    def has_comment(self):
        if len(self.comment_set.all()) != 0:
            return True
        else:
            return False
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    news_id = models.ForeignKey(News, on_delete=models.CASCADE)
    author_of_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.content