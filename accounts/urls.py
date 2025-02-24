from django.urls import path
from . import views
from .views import change_password

app_name = 'accounts'

urlpatterns = [
    path("signup/", views.signup_page, name="signup"),
    path("login/", views.login_page, name="login"),
    path("email_verification/<uuid:token>", views.email_verification, name="email_verification"),
    path("profile/", views.profile_page, name="profile"),
    path('change_username/', views.change_username, name='change_username'),
    path('change_password/', change_password, name='change_password'),
]
