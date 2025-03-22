from django.urls import path
from . import views

app_name = 'leaderboards'

urlpatterns = [
    path("", views.leaderboard, name="leaderboard"),
    path("daily-streaks", views.daily_streak_leaderboard, name="daily_streak_leaderboard")
]
