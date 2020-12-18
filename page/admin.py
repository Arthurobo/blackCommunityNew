from django.contrib import admin

from .models import Page, Post, Comment

admin.site.register(Page)
admin.site.register(Post)
admin.site.register(Comment)