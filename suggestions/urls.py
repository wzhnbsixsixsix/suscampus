from django.urls import path

from . import views

urlpatterns = [
    path("", views.suggestions, name="suggestions"),
    # 在urlpatterns中添加
    path('view-suggestions/', views.view_suggestions, name='view_suggestions'),
    path('delete-suggestion/<int:suggestion_id>/', views.delete_suggestion, name='delete_suggestion'),
]
