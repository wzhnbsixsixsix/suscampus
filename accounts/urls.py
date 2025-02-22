from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path("signup/", views.signup_page, name="signup"),
    path("login/", views.login_page, name="login"),
    path("email_verification/<uuid:token>", views.email_verification, name="email_verification"),
    path("profile/",views.setting_page,name="profile"),
]

