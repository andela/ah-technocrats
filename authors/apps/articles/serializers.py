from rest_framework import serializers
from rest_framework.exceptions import ParseError

from authors.apps.profiles.serializers import ProfileSerializer
from .models import Article, Rating, ReportArticle, Comment, Reply, BookMarkArticle
from ..authentication.serializers import UserSerializer
from ..authentication.models import User
from rest_framework.validators import UniqueTogetherValidator

class ArticleTagSerializer(serializers.Field):
    """
    class for handling article tags serialization.
    """
    def to_internal_value(self, data):
        if type(data) is not list:
            raise ParseError("Expect 'tags' to be a list." )
        return data

    def to_representation(self, obj):
        if type(obj) is not list:
            return [tag for tag in obj.all()]
        return obj


class ArticleSerializer(serializers.ModelSerializer):
    """
    Class to serialize article details.
    """
    tags = ArticleTagSerializer(default=[])
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    body = serializers.CharField()
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
  
    class Meta:
        """
        Method defines what fields of an article object should be displayed.
        """
        model = Article
        fields = ("title", "description", "body", "author", "tags")

    def validate_tagList(self, validated_data):
        if type(validated_data) is not list:
            raise serializers.ValidationError("not  valid")
        return validated_data

    def create(self, data, *args):
        """
        Method enables the creation of an article.
        """
        new_article = Article(**data)
        new_article.save()
        article = Article.objects.get(pk=new_article.pk)
        for tag in new_article.tags:
            article.tags.add(tag)
        return new_article

    def update(self, instance, data):
        """
        Method enables the editing of an article.
        """
        instance.title = data.get('title', instance.title)
        instance.description = data.get('description', instance.description)
        instance.body = data.get('body', instance.body)
        instance.author_id = data.get('authors_id', instance.author_id)
        if 'tagList' not in data:
            return instance
        instance.tagList = data.get('tagList')
        article = Article.objects.get(pk=instance.pk)
        article.tagList.set(*instance.tagList, clear=True)
        # instance.save()
        return instance

    def get_author(self, Article):
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
    tags = serializers.SerializerMethodField(method_name='show_tags')
    

    def show_tags(self, instance):
        """
        Show tag details.
        """
        return instance.tags.names()
        

    def likes(self, instance):
        """method to return a user who has liked an article"""
        request = self.context.get('request')
        liked = False
        if request is not None and request.user.is_authenticated:
            user_id = request.user.id
            liked = instance.likes.all().filter(id=user_id).count() == 1
        return {'likes': instance.likes.count(), 'User': liked}

    def dislikes(self, instance):
        """method to return a user who has disliked an article"""
        request = self.context.get('request')
        disliked = False
        if request is not None and request.user.is_authenticated:
            user_id = request.user.id
            disliked = instance.dislikes.all().filter(id=user_id).count() == 1
        return {'dislikes': instance.dislikes.count(), 'User': disliked}

    favorite = serializers.SerializerMethodField(read_only=True)

    def favorite(self, instance):
        """favorite an article"""
        request = self.context.get('request')
        favorite = False
        if request is not None and request.user.is_authenticated:
            user_id = request.user.id
            favorite = instance.favorite.all().filter(id=user_id).count() == 1
        return {'favoritesCount': instance.favorite.count(), 'favorite': favorite}

    class Meta:
        model = Article
        # fields = ('title', 'description', 'body', 'like', 'dislike', 'favorite','author')
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
            highlight_start=self.context['start'],
            highlight_end=self.context['end'],
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


class RatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(source='rating.value',
                                      required=True, allow_null=False, )

    class Meta:
        model = Rating
        fields = ('rating',)


class ReportArticleSerializer(serializers.ModelSerializer):
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())
    reported_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    report = serializers.ChoiceField(choices=ReportArticle.REPORT_CHOICES)

    class Meta:
        model = ReportArticle
        fields = ('article', 'reported_by', 'report')

class BookMarkArticleSerializer(serializers.ModelSerializer):
    """
    class to serialize bookmarked articles
    """
    article_slug = serializers.CharField(source='article.article_slug')
    class Meta:
        model = BookMarkArticle
        fields = [
            'article_slug',
            'id'
        ]