from django.urls import path
from twitteruser import views

urlpatterns = [
    path("", views.Index.as_view(), name="home"),
    path(
        "users/<slug:slug>/",
        views.TwitterUserDetail.as_view(),
        name="twitter_user_details",
    ),
    path("notifications/", views.notifications, name="notifications"),
    path("follow/<slug:slug>/", views.follow_user, name="follow_user"),
    path("unfollow/<slug:slug>/", views.unfollow_user, name="unfollow_user"),
]
