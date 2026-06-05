from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'is_active', 'show_on_login', 'show_on_dashboard']
    list_filter = ['is_active', 'show_on_login', 'show_on_dashboard']
    search_fields = ['title', 'content']