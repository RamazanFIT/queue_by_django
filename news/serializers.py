from rest_framework import serializers
from .models import News




class NewsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ["id", "title", "content", "created_at", "author_of_news"]






