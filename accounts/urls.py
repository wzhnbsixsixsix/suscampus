from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup_page, name="signup"),
    path("login/", views.login_page, name="login"),
    path("email_verification/<uuid:token>", views.email_verification, name="email_verification"),
]

