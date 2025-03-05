from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')  # Fields to display
   # list_editable = ('created_at',)  # Make created_at editable
    search_fields = ('title', 'summary', 'content')  # Make the title and content searchable