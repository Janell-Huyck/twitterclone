from django.urls import path
from twitteruser import views

urlpatterns = [
    path("", views.index, name="home"),
    path("users/<slug:slug>/", views.twitterUserDetail, name="twitter_user_detail"),
    path("notifications/", views.notifications, name="notifications"),
]
