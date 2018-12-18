from rest_framework.generics import CreateAPIView, ListAPIView
from authors.apps.articles.models import BookMarkArticle, Article
from rest_framework.response import Response
from rest_framework import status
from authors.apps.articles.exceptions import ArticleNotFound
from authors.apps.articles.serializers import BookMarkArticleSerializer


class BookMarkCreateAPIView(CreateAPIView):
    """
    bookmark and unbookmark an article
    """
    serializer_class = BookMarkArticleSerializer

    def post(self, request, article_slug):
        """
        confirm if the article is already bookmarked, 
        if not, bookmark it.
        """
        user = request.user
        try:
            article = Article.objects.get(article_slug=article_slug)
        except Article.DoesNotExist:
            raise ArticleNotFound()
        bookmark, created = BookMarkArticle.objects.get_or_create(
            user=user,
            article=article
        )
        if not created:
            """
            if article already bookmarked, then delete it
            """
            bookmark.delete()
        """create article bookmark"""
        return Response(
            {
                'message': 'Article bookmarked successfully',
            }, 
            status=status.HTTP_201_CREATED,
        ) if created else \
            Response(
                {
                    'message': 'Bookmark deleted successfully',
                },
                status=status.HTTP_200_OK
            )

class BookMarkListAPIView(ListAPIView):
    """
    get all bookmarked articles
    """

    def list(self, request):
        """
        get all bookmarked articles
        """
        queryset = BookMarkArticle.objects.select_related('article', 'article__author', 'user__profile') \
            .filter(user=request.user)
        serializer = BookMarkArticleSerializer(queryset, many=True)
        return Response(
            {
                'bookmarked articles': serializer.data,
                'count': len(serializer.data)
            },
            status=status.HTTP_200_OK
        ) if len(serializer.data) else \
            Response(
                {
                    'message': 'No articles bookmarked yet.'
                },
                status=status.HTTP_200_OK
            )