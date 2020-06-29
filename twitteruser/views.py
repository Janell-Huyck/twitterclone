from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from twitteruser.models import TwitterUser
from tweet.models import Tweet
from notification.models import Notification
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin


class Index(LoginRequiredMixin, View):
    html = "../templates/index.html"

    def get(self, request):
        """Return a view with the profile block, all tweets made
        by the user and all users followed"""

        user = request.user
        profile_details = userDetailBlock(user.slug)
        followed_authors = user.following.all()

        # Notifications count goes on menu bar
        user_notifications = Notification.objects.filter(
            victim=user, viewed=False
        ).count()

        # Tweets shown needs to include user's and followed authors'
        user_tweets = Tweet.objects.filter(author=user)
        tweets = [user_tweet for user_tweet in user_tweets]
        for followed_author in followed_authors:
            their_tweets = Tweet.objects.filter(author=followed_author)
            tweets.extend(their_tweets)

        context = {
            "user": user,
            "profile_details": profile_details,
            "tweets": tweets,
            "user_notifications": user_notifications,
        }

        return render(request, self.html, context)


def userDetailBlock(slug):
    details = {}
    user = get_object_or_404(TwitterUser, slug=slug)
    details["user"] = user
    tweet_count = Tweet.objects.filter(author=user).count
    details["tweet_count"] = tweet_count
    notifications = Notification.objects.filter(victim=user, viewed=False).count()
    details["notifications"] = notifications
    follow_count = user.following.count()
    details["follow_count"] = follow_count

    return details


class TwitterUserDetail(View):
    html = "../templates/index.html"

    def get(self, request, slug):
        detailed_user = TwitterUser.objects.get(slug=slug)
        profile_details = userDetailBlock(detailed_user.slug)
        tweets = Tweet.objects.filter(author=detailed_user)
        user_is_following = detailed_user in request.user.following.all()

        if user_is_following:
            follow_url = "unfollow_user"
            follow_text = "Unfollow User"
            follow_button_class = "btn btn-danger"
        else:
            follow_url = "follow_user"
            follow_text = "Follow User"
            follow_button_class = "btn btn-primary"

        context = {
            "detailed_user": detailed_user,
            "profile_details": profile_details,
            "tweets": tweets,
            "follow_url": follow_url,
            "follow_text": follow_text,
            "follow_button_class": follow_button_class,
        }
        return render(request, self.html, context)


def notifications(request):
    context = {}
    user = request.user
    context["user"] = user
    profile_details = userDetailBlock(user.slug)
    context["profile_details"] = profile_details
    notifications = Notification.objects.filter(victim=user, viewed=False)
    context["tweets"] = notifications
    for notification in notifications:
        notification.viewed = True
        notification.save()
    return render(request, "../templates/index.html", context)


def follow_user(request, slug):
    current_user = request.user
    current_user.following.add(TwitterUser.objects.get(slug=slug))
    return HttpResponseRedirect(reverse("twitter_user_details", kwargs={"slug": slug}))


def unfollow_user(request, slug):
    current_user = request.user
    current_user.following.remove(TwitterUser.objects.get(slug=slug))
    return HttpResponseRedirect(reverse("twitter_user_details", kwargs={"slug": slug}))
