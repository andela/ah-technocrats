from rest_framework import serializers

from ..authentication.serializers import UserSerializer
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """
    Class to serialize article details.
    """
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    body = serializers.CharField()
    author = serializers.HiddenField(
        default = serializers.CurrentUserDefault()
    )

    class Meta:
        """
        Method defines what fields of an article object should be displayed.
        """
        model = Article
        fields = '__all__'

    def create(self, data):
        """
        Method enables the creation of an article.
        """
        return Article.objects.create(**data)

    def update(self, instance, data):
        """
        Method enables the editing of an article.
        """
        instance.title = data.get('title', instance.title)
        instance.description = data.get('description', instance.description)
        instance.body = data.get('body', instance.body)
        instance.author_id = data.get('authors_id',instance.author_id)
        instance.save()
        return instance

    def get_author(self,Article):
        """
        Method to get the author of an article.
        """
        return Article.author.pk

class ArticleAuthorSerializer(serializers.ModelSerializer):
    """
    Class to serialize article and return the full owner information.
    """
    # Since the author field is hidden in ArticleSerializer, 
    # this method displays the author details associated with the article
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    body = serializers.CharField()
    author = UserSerializer(read_only = True)
    class Meta:
        model = Article
        fields = '__all__'
    