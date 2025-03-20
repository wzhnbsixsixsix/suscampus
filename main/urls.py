from django.urls import path

from.import views

app_name = 'main'

urlpatterns = [
    path('', views.first_page, name='first_page'), # First page the website should lead to when accessed
    path('map/', views.map, name='map'),
    path('forest/', views.forest, name='forest'),
    path('forest/save', views.save_forest, name='save_forest'),
    path('forest/handle_recycling', views.handle_recycling, name='handle_recycling'),
    path('forest/get_recycled_count', views.get_recycled_count, name='get_recycled_count'),
    path('map/claim_blue_marker', views.claim_blue_marker, name='claim_blue_marker'),
    path('map/claim_red_marker', views.claim_red_marker, name='claim_red_marker'),
    path('map/claim_green_marker', views.claim_green_marker, name='claim_green_marker'),
    path('map/update_inv_on_page', views.update_inv_on_page, name='update_inv_on_page')
]
