from django.contrib import admin

from .models import Content, ContentScore


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at')
    search_fields = ('title',)


@admin.register(ContentScore)
class ContentScoreAdmin(admin.ModelAdmin):
    list_display = ('content', 'score', 'created_at')
    search_fields = ('content', 'score')
