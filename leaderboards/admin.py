from django.contrib import admin
from .models import TreeScore

# Register your models here.
class TreeScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score') 
    search_fields = ('user__username',)

admin.site.register(TreeScore, TreeScoreAdmin)