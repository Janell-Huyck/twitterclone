from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from twitteruser.models import TwitterUser
from tweet.models import Tweet
from notification.models import Notification


@login_required
def index(request):
    context = {}
    user = request.user
    context["user"] = user
    profile_details = userDetailBlock(user.slug)
    context["profile_details"] = profile_details
    tweets = []
    user_tweets = Tweet.objects.filter(author=user)
    for user_tweet in user_tweets:
        tweets.append(user_tweet)
    followed_authors = user.following.all()
    for followed_author in followed_authors:
        their_tweets = Tweet.objects.filter(author=followed_author)
        tweets.extend(their_tweets)
    context["tweets"] = tweets
    return render(request, "../templates/index.html", context)


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


def twitterUserDetail(request, slug):
    context = {}
    detailed_user = TwitterUser.objects.get(slug=slug)
    context["detailed_user"] = detailed_user
    profile_details = userDetailBlock(detailed_user.slug)
    context["profile_details"] = profile_details
    tweets = Tweet.objects.filter(author=detailed_user)
    context["tweets"] = tweets
    user_is_following = detailed_user in request.user.following.all()
    if user_is_following:
        follow_url = "unfollow_user"
        follow_text = "Unfollow User"
        follow_button_class = "btn btn-danger"
    else:
        follow_url = "follow_user"
        follow_text = "Follow User"
        follow_button_class = "btn btn-primary"
    context["follow_url"] = follow_url
    context["follow_text"] = follow_text
    context["follow_button_class"] = follow_button_class
    return render(request, "../templates/index.html", context)


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
