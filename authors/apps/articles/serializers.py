from rest_framework import serializers

from ..authentication.serializers import UserSerializer
from .models import Article, Comment, Reply
from authors.apps.profiles.serializers import ProfileSerializer


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

class ReplySerializer(serializers.ModelSerializer):
    """
    serialize reply model data
    """
    author = ProfileSerializer(required=False)
    class Meta:
        """
        serializer attributes
        """
        model = Reply
        exclude = ('comment',) 

    def create(self, validated_data):
        """
        create a new reply for an article comment
        """
        return Reply.objects.create(
            author=self.context['author'],
            comment=self.context['comment'],
            **validated_data
        ) 
    
    def update(self, instance, validated_data):
        """
        method for updating an comment's reply
        """
        instance.body = validated_data.get('body', instance.body)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance
class CommentSerializer(serializers.ModelSerializer):
    """
    class to serialize comments data
    """
    author = ProfileSerializer(required=False)
    created_at = serializers.SerializerMethodField(method_name='get_formated_create_at')
    last_update = serializers.SerializerMethodField(method_name='get_formated_last_update')
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        """
        define serializer attributes
        """
        model = Comment
        fields = (
            'id',
            'author',
            'body',
            'created_at',
            'last_update',
            'replies'
        )

    def create(self, validated_data):
        """
        create a new comment for an article
        """
        return Comment.objects.create(
            author=self.context['author'],
            article=self.context['article'],
            **validated_data
        )

    def update(self, instance, validated_data):
        """
        method for updating an articles' comment
        """
        instance.body = validated_data.get('body', instance.body)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance

    def get_formated_create_at(self, instance):
        """
        return formated create_at time for a comment
        """
        return instance.created_at.isoformat()
    
    def get_formated_last_update(self, instance):
        """
        return formated last_update time for a comment
        """
        return instance.last_update.isoformat()
