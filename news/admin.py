from django.contrib import admin
from .models import News, Comment


admin.site.register(Comment)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 5 


class AdminNews(admin.ModelAdmin):
    fields = ["title", "content"]
    inlines = [CommentInline]
    list_display = ["title", "content", "created_at", "has_comment"]
    list_filter = ["created_at"]


admin.site.register(News, AdminNews)