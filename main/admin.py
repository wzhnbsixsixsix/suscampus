from django.contrib import admin
from .models import UserInventory, UserForest, Plant, UserHighScore

class UserInventoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'paper', 'plastic', 'compost', 'recycled_paper', 'recycled_plastic', 'recycled_compost', 'tree_guard', 'rain_catcher', 'fertilizer', 'oak', 'birch', 'fir', 'red_campion', 'poppy', 'cotoneaster')
    search_fields = ('user__username', 'user__email') 

class UserForestAdmin(admin.ModelAdmin):
    list_display = ('user', 'cells', 'last_growth_check_date')
    search_fields = ('user__username', 'user__email')

class PlantAdmin(admin.ModelAdmin):
    list_display = ('plant_name', 'requirement_type', 'rarity')
    search_fields = ('plant_name',)

class UserHighScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'high_score')
    search_fields = ('user__username',)

# Register models with the admin interface
admin.site.register(UserInventory, UserInventoryAdmin)
admin.site.register(UserForest, UserForestAdmin)
admin.site.register(Plant, PlantAdmin)
admin.site.register(UserHighScore, UserHighScoreAdmin)