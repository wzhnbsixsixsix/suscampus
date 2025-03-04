
# urls.py

from django.urls import path
from . import views
from .views import like_announcement, dislike_announcement



urlpatterns = [
    path('', views.announcement_list, name='announcement_list'),
    path('create/', views.create_announcement, name='create_announcement'),
    path('announcement/<int:announcement_id>/like/', like_announcement, name='like_announcement'),
    path('announcement/<int:announcement_id>/dislike/', dislike_announcement, name='dislike_announcement'),

]

