from django.urls import path

from . import views

urlpatterns = [
    path("", views.suggestions, name="suggestions"),
    path("view/", views.view_suggestions, name="view_suggestions"),

]
