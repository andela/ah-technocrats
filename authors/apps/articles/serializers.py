from rest_framework import serializers

from .models import Article
from ..authentication.serializers import UserSerializer


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
        model = Article
        fields = '__all__'

    def create(self, data):
        return Article.objects.create(**data)

    def update(self, instance, data):
        instance.title = data.get('title', instance.title)
        instance.description = data.get('description', instance.description)
        instance.body = data.get('body', instance.body)
        instance.author_id = data.get('authors_id',instance.author_id)
        instance.save()
        return instance

    def get_author(self,Article):
        return Article.author.pk

class ArticleAuthorSerializer(serializers.ModelSerializer):
    """
    Class to serialize article and return the full owner information.
    """
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    body = serializers.CharField()
    author = UserSerializer(read_only = True)
    class Meta:
        model = Article
        fields = '__all__'
    