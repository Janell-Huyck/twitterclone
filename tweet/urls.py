from django.urls import path
from tweet import views

urlpatterns = [
    path("<int:pk>/", views.TweetDetail.as_view(), name="tweet_detail"),
    path("new_tweet/", views.NewTweet.as_view(), name="new_tweet"),
]
