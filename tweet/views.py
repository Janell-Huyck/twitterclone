from django.shortcuts import render
from tweet.models import Tweet
from notification.models import Notification
from tweet.forms import NewTweetForm
from twitteruser.models import TwitterUser
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
import re
from django.views.generic.base import View


class TweetDetail(View):
    def get(self, request, pk):
        tweet = Tweet.objects.get(pk=pk)
        html = "../templates/tweet_detail.html"
        return render(request, html, {"tweet": tweet})


class NewTweet(View):
    html = "../templates/general_form.html"

    def get(self, request):
        form = NewTweetForm()
        return render(request, self.html, {"form": form})

    def post(self, request):
        form = NewTweetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_tweet = Tweet.objects.create(
                author=TwitterUser.objects.get(username=request.user.username),
                text=data["text"],
                tweet_time=timezone.now(),
            )
            new_tweet.save()
            victims = re.findall("@(\\S*\\b)", data["text"])
            for new_victim in victims:
                new_notification = Notification.objects.create(
                    victim=TwitterUser.objects.get(username=new_victim[:]),
                    tweet_id=Tweet.objects.get(pk=new_tweet.pk),
                    viewed=False,
                )
                new_notification.save()
            return HttpResponseRedirect(reverse("home"))
        return render(request, self.html, {"form": form})


# def newTweet(request):
#     if request.method == "POST":
#         form = NewTweetForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             new_tweet = Tweet.objects.create(
#                 author=TwitterUser.objects.get(username=request.user.username),
#                 text=data["text"],
#                 tweet_time=timezone.now(),
#             )
#             new_tweet.save()
#             victims = re.findall("@(\\S*\\b)", data["text"])
#             print("tweet created")
#             for new_victim in victims:
#                 new_notification = Notification.objects.create(
#                     victim=TwitterUser.objects.get(username=new_victim[:]),
#                     tweet_id=Tweet.objects.get(pk=new_tweet.pk),
#                     viewed=False,
#                 )
#                 new_notification.save()
#                 print("new notification created")
#             return HttpResponseRedirect(reverse("home"))
#     form = NewTweetForm()
#     return render(request, "../templates/general_form.html", {"form": form})
