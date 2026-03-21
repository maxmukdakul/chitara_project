from django.contrib import admin
from .models import User, Song, Notification

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'daily_generate_count', 'last_generate_date')
    search_fields = ('name', 'email')

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'genre', 'generation_status', 'created_at')
    list_filter = ('generation_status', 'genre', 'voice_type')
    search_fields = ('title', 'user__name')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('action_type', 'user', 'timestamp')
    list_filter = ('action_type', 'timestamp')