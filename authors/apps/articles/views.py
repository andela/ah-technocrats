from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from requests.exceptions import HTTPError

from .permissions import IsOwnerOrReadOnly
from .models import Article
from .serializers import ArticleSerializer, ArticleAuthorSerializer


class ArticleAPIView(APIView):
    """ 
    Class for handling Article.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        """
        Method for creating an article
        """
        article_data = request.data.get('article')
        context = {'request':request}
        serializer = ArticleSerializer(data=article_data, context=context)
        serializer.is_valid(raise_exception=True)
        saved_article = serializer.save()
        message = {'message': "The article '{}' has been successfully created.".format(saved_article.title),
        'title':saved_article.title,
        'slug': saved_article.article_slug}
        return Response(message, status=status.HTTP_201_CREATED)
              
    def get(self, request):
        """
        Method for getting all articles.
        """
        # It gets a specific article using the slug that is provided in the url
        articles = Article.objects.all()
        if articles:
            serializer = ArticleAuthorSerializer(articles, many=True)
            message = {'message':"Articles found.", 'articles': serializer.data}
            return Response(message, status=status.HTTP_200_OK)
        else:
            return Response({'message':"Articles not found"})


class SpecificArticleAPIView(APIView):
    """
    Class for handling a single article.
    """
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def get(self,request, slug):
        """
        Method for getting one article.
        """
        article = Article.objects.get(article_slug=slug)
        serializer = ArticleAuthorSerializer(article)
        message = {'message':"Article found.", 
            'article':serializer.data}
        return Response(message, status=status.HTTP_200_OK)

    def put(self, request, slug):
        
        """
        Method for editing an article.
        """
        # A slug should be provided.
        # An article should be edited by the person who created it only.
        article = Article.objects.get(article_slug=slug)
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
                'message':"article '{}' has been successfully deleted.".format(article_details.title)            
                }
            return Response(message, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message':"article not found."})
