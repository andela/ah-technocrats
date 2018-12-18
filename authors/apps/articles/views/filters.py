from django_filters import rest_framework as filters
from rest_framework.generics import  ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny


from authors.apps.articles.serializers import  ArticleAuthorSerializer
from authors.apps.articles.models import Article



class FilterSearchViewset(ViewSet):
    """Viewset to filter through articles."""
    serializer_class = ArticleAuthorSerializer
    permission_classes = (AllowAny,)
    # filter_backends = (SearchFilter,)
    # search_fields = ('title')

 
    def list(self, request):
        """Get a list of articles with searched query."""
        queryset = Article.objects.all()


        queries = {
            'tag': request.GET.get('tag'),
            'title': request.GET.get('title'),
            'author': request.GET.get('author'),
            'search': request.GET.get('search')}
        if queries['tag']:
            result = queryset.filter(
                Q(tags__name__icontains=queries['tag']))
        elif queries['title']:
            result = queryset.filter(
                Q(title__icontains=queries['title']))
        elif queries['author']:
            result = queryset.filter(
                Q(author__username__icontains=queries['author']))
        elif queries['search']:
            result = Article.objects.filter(
                Q(tags__name__icontains=queries['search'])|
                Q(title__icontains=queries['search'])|
                Q(author__username__icontains=queries['search'])
            )
        else:
            data = {"message": "Missing search query."}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        if result:
            serializers = [ArticleAuthorSerializer(i).data for i in result]
            return Response(data=serializers, status=status.HTTP_200_OK)
        else:
            data = {"message": "Your search has not been found."}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)


