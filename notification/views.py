from django.shortcuts import render
from notification.models import Notification
from tweet.models import Tweet


def showNotifications(request):
    user = request.user
    notifications_objects = Notification.objects.filter(victim=user, viewed=False)
    notifications = []
    for notification in notifications_objects:
        tweet = Tweet.objects.get(pk=notification.tweet_id.pk)
        notifications.append(tweet)
    return render(
        request, "../templates/notifications.html", {"notifications": notifications}
    )
