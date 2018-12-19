from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from authors.apps.articles.models import Article
from authors.apps.articles.serializers import ArticleSerializer


class FavoriteArticles(UpdateAPIView):
    """Class for making an article a favorite"""
    serializer_class = ArticleSerializer

    def update(self, request, slug):
        """This method updates the making of an article a favorite"""
        try:
            article = Article.objects.get(article_slug=slug)
        except Article.DoesNotExist:
            return Response({
                'Error': 'Article does not exist'
            }, status.HTTP_404_NOT_FOUND)

        # gets the user of that specific session
        user = request.user

        # checks for the boolean value of making an article a favorite
        confirm = bool(user in article.favorite.all())
        if confirm is True:
            article.favorite.remove(user.id)
            message = {"Success": "You have removed this article from your favorites"}
            return Response(message, status.HTTP_200_OK)

        # if favoriting is false, the article is made a favorite
        article.favorite.add(user.id)
        message = {"Success": "This article is a favourite"}
        return Response(message, status.HTTP_200_OK)
