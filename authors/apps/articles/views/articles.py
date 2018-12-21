from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.settings import api_settings

from authors import settings
from authors.apps.articles.models import Article
from authors.apps.articles.permissions import IsOwnerOrReadOnly
from authors.apps.articles.serializers import ArticleSerializer, ArticleAuthorSerializer
from authors.apps.authentication.models import User
from authors.apps.notifications.models import follower_notification


@receiver(post_save, sender=Article)
def notify_followers(sender, instance, created, **kwargs):
    """
    send a message notification upon creation of an article.
    """
    if created:
        message = (instance.title + " has been successfully created by " + instance.author.username)
        follower_notification(instance.author, message, instance)


class ArticleAPIView(APIView):
    """
   Class for handling Article.
   """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def post(self, request):
        """
       Method for creating an article
       """
        article_data = request.data.get('article')
        context = {'request': request}
        serializer = ArticleSerializer(data=article_data, context=context)
        serializer.is_valid(raise_exception=True)
        saved_article = serializer.save()
        message = {'message': "The article '{}' has been successfully created.".format(saved_article.title),
                   'title': saved_article.title,
                   'slug': saved_article.article_slug}

        # Sending an email to followers who requested notifications.
        author_profile = User.objects.get(email=request.user).profile
        followers = author_profile.user_following.all()
        if request.is_secure():
            protocol = "https://"
        else:
            protocol = "http://"
        host = request.get_host()
        path = reverse("authentication:user-login")
        link = protocol + host + path

        for follower in followers:
            if follower.notifications_enabled is True:
                user = follower.user.username
                msg_plain = render_to_string('notification_email.txt', {
                    'user': user,
                    'title': saved_article.title,
                    'author': author_profile.user.username,
                    "link": link
                })
                msg_html = render_to_string('notification_email.html', {
                    'user': user,
                    'title': saved_article.title,
                    'author': author_profile.user.username,
                    'link': link
                })
                send_mail(
                    'New Article Notification',
                    msg_plain,
                    settings.EMAIL_HOST_USER,
                    [follower.user.email],
                    html_message=msg_html,
                )
        return Response(message, status=status.HTTP_201_CREATED)

    def get(self, request):
        """
        Method for getting all articles.
        """
        # set up pagination
        articles = Article.objects.all()
        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = ArticleAuthorSerializer(page, many=True)
            message = {'articles': serializer.data}
            return self.get_paginated_response(message)
                
    @property
    def paginator(self):
        """
        define the paginator method.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, articles):
        """
        Return the page if the paginator is enabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(articles, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Print out the results with the link to previous and next page.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class SpecificArticleAPIView(APIView):
    """
    Class for handling a single article.
    """
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def get(self, request, slug):
        """
        Method for getting one article.
        """
        article = Article.objects.filter(article_slug=slug).first()
        final = dict()
        serializer = ArticleAuthorSerializer(article)
        final.update(serializer.data)
        final.update({"rating": article.rating})
        message = {'message': "Article found.", 'article': final}
        if article is None:
            return Response({"message": "Article not found, Please check your slug"}, status=status.HTTP_404_NOT_FOUND)
        return Response(message, status=status.HTTP_200_OK)

    def put(self, request, slug):

        """
        Method for editing an article.
        """
        # A slug should be provided.
        # An article should be edited by the person who created it only.
        article = Article.objects.filter(article_slug=slug).first()
        if article is None:
            return Response({"message": "Article not found with that slug"}, status=status.HTTP_404_NOT_FOUND)
        if request.user.pk != article.author_id:
            return Response({'Error': "You are not allowed to perform this request."},
                            status=status.HTTP_403_FORBIDDEN)
        data = request.data.get('article')
        serializer = ArticleSerializer(instance=article, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        article = serializer.save()
        message = {
            'message': "Article has been successfully updated.",
            'article_title': article.title
        }
        return Response(message, status=status.HTTP_200_OK)

    def delete(self, request, slug):
        """
        Delete a specific item.
        """
        try:
            article_details = Article.objects.get(article_slug=slug)
            if article_details:
                if request.user.pk != article_details.author_id:
                    message = {'Error': "You are not allowed to delete this article."}
                    return Response(message, status=status.HTTP_403_FORBIDDEN)
            article_details.delete()
            message = {
                'message': "article '{}' has been successfully deleted.".format(article_details.title)
            }
            return Response(message, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': "article not found."})

class LikeArticle(UpdateAPIView):
    """Class for liking and un -liking an article"""

    def update(self, request, slug):
        """This method updates the liking of an article"""
        try:
            article = Article.objects.get(article_slug=slug)
        except Article.DoesNotExist:
            return Response({
                'Error': 'Article does not exist'
            }, status.HTTP_404_NOT_FOUND)

        # gets the user of that specific session
        user = request.user
        # checks for the boolean value of liking an article
        liked = bool(user in article.like.all())
        if liked is True:
            article.like.remove(user.id)
            message = {"article": "You have unliked this article"}
            return Response(message, status.HTTP_200_OK)

        # if like is false, the article is liked
        disliked = bool(user in article.dislike.all())
        if disliked is True:
            article.dislike.remove(user.id)

        article.like.add(user.id)
        message = {"article": "You have liked this article"}
        return Response(message, status.HTTP_200_OK)


class DislikeArticle(UpdateAPIView):
    """Class for disliking and  un-disliking an article"""

    def update(self, request, slug):
        """This method updates the disliking of an article"""
        try:
            article = Article.objects.get(article_slug=slug)
        except Article.DoesNotExist:
            return Response({
                'Error': 'Article does not exist'
            }, status.HTTP_404_NOT_FOUND)

        # gets the user of that specific session
        user = request.user
        # checks for the boolean value of disliking an article
        disliked = bool(user in article.dislike.all())
        if disliked is True:
            article.dislike.remove(user.id)
            message = {"article": "This article has been un-disliked"}
            return Response(message, status.HTTP_200_OK)

        # if disike is false, the article is disliked
        liked = bool(user in article.like.all())
        if liked is True:
            article.like.remove(user.id)
            
        article.dislike.add(user.id)
        message = {"article": "You have disliked this article"}
        return Response(message, status.HTTP_200_OK)
