from django.contrib import admin
from .models import Announcement, Message


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'school', 'audience', 'posted_by', 'created_at')
    list_filter = ('school', 'audience')
    search_fields = ('title', 'content')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'is_warning', 'is_read', 'created_at')
    list_filter = ('school', 'is_warning', 'is_read')
    search_fields = ('subject', 'content', 'sender__username', 'recipient__username')