from django.contrib import admin

from .models import Channel
# Register your models here.
class channel(admin.ModelAdmin):
    list_display = ("channel_id","title","subs")

admin.site.register(Channel,channel)  