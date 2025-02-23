from django.urls import path

from.import views

app_name = 'main'

urlpatterns = [
    path("", views.map, name="map"),
    path("forest/", views.forest, name="forest")
]
