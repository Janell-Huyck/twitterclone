from django.urls import path
from authentication import views

urlpatterns = [
    path("login/", views.loginView, name="login"),
    path("logout/", views.logoutView, name="logout"),
    path("signup/", views.signupView, name="signup"),
]
