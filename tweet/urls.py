from django.urls import path
from tweet import views

urlpatterns = [
    path("<int:pk>/", views.tweetDetail, name="tweet_detail"),
    path("new_tweet/", views.newTweet, name="new_tweet"),
]
