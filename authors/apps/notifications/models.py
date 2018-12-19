from django.db import models
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article, Comment


class Notification(models.Model):
    """
    Database fields for the notifications
    """

    article = models.ForeignKey(Article, blank=True, null=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, blank=True, null=True, on_delete=models.CASCADE)
    # article = models.TextField(blank=True)
    notification = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    notified = models.ManyToManyField(
        User, related_name='notified', blank=True)
    notify_comments = models.ManyToManyField(
        User, related_name='notify_comments', blank=True)
    read = models.ManyToManyField(User, related_name='read', blank=True)
    classification = models.TextField(default="article")

    def __str__(self):
        return self.notification


def follower_notification(author, notification, article):
    """
    This function adds notification to the Notification model
    Checks if the user is in the list to be notified
    """
    notification = Notification.objects.create(
        notification=notification, classification="article", article=article)
    profile = author.profile
    followers = profile.user_following.all()
    for follower in followers:
        if follower.notifications_enabled is True:
            notification.notified.add(follower.user.id)
    notification.save()


def favorites_notification(favorited, notification, comment):
    """
    Function that adds a notification to the Notification model.
    Loops to check the author's followers profiles where notification is on
    in order to add them to the notified column of the notification.
    """
    notification = Notification.objects.create(
        notification=notification, classification="comment")
    favorites = comment.article.favorite.all()
    for favorite in favorites:
        if favorite.profile.notifications_enabled is True:
            notification.notify_comments.add(favorite.profile.user_id)
    notification.save()
