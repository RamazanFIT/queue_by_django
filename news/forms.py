from django import forms
from django.forms import ModelForm
from .models import News




class NewsAddModelForm(ModelForm):
    class Meta():
        model = News
        fields = ["title", "content"] 

