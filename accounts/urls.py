from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signUpPage, name="signup"),
    path("login/", views.loginPage, name="login"),
    path("email_verification/<uuid:token>", views.email_verification, name="email_verification"),
]