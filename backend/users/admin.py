from django.contrib import admin
from .models import Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'user',)
    list_filter = ('author', 'user',)
    search_fields = ('user',)
    empty_value_display = '-пусто-'
