from django.contrib import admin
from .models import TreeScore

# Register your models here.
class TreeScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score')  # Fields to display in the list view
    search_fields = ('user__username',)  # Enable search by username

admin.site.register(TreeScore, TreeScoreAdmin)