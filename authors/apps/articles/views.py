from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView, DestroyAPIView, UpdateAPIView
)
from django.db.utils import Error
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.apps.articles.models import Rating
from .models import Article
from .models import Comment, Reply
from .permissions import IsOwnerOrReadOnly
from .serializers import ArticleSerializer, ArticleAuthorSerializer
from .serializers import (
    CommentSerializer,
    ReplySerializer
)
from .serializers import (
    RatingSerializer)
from .models import Article
from .serializers import ArticleSerializer, ArticleAuthorSerializer
from rest_framework.generics import UpdateAPIView


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
        context = {'request': request}
        serializer = ArticleSerializer(data=article_data, context=context)
        serializer.is_valid(raise_exception=True)
        saved_article = serializer.save()
        message = {'message': "The article '{}' has been successfully created.".format(saved_article.title),
                   'title': saved_article.title,
                   'slug': saved_article.article_slug}
        return Response(message, status=status.HTTP_201_CREATED)

    def get(self, request):
        """
        Method for getting all articles.
        """
        # It gets a specific article using the slug that is provided in the url
        articles = Article.objects.all()
        if articles:
            result = []
            for article in articles:
                individual = dict()
                individual.update(ArticleAuthorSerializer(article).data)
                individual.update({"rating": article.just_average})
                result.append(individual)
            message = {'message': "Articles found.", 'articles': result}
            return Response(message, status=status.HTTP_200_OK)
        else:
            return Response({'message': "Articles not found"})


class SpecificArticleAPIView(APIView):
    """
    Class for handling a single article.
    """
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def get(self, request, slug):
        """
        Method for getting one article.
        """
        article = Article.objects.get(article_slug=slug)
        final = dict()
        serializer = ArticleAuthorSerializer(article)
        final.update(serializer.data)
        final.update({"rating": article.rating})
        message = {'message': "Article found.", 'article': final}
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
                'message': "article '{}' has been successfully deleted.".format(article_details.title)
            }
            return Response(message, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': "article not found."})


class CommentsListAPIView(ListCreateAPIView):
    """
    get comment for a given article and create comment for an
    article
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'article__article_slug'
    lookup_url_kwarg = 'article_slug'
    serializer_class = CommentSerializer
    queryset = Comment.objects.select_related(
        'article', 'article__author', 'article__author__profile',
        'author', 'author__user'
    )

    def create(self, request, article_slug=None):
        """
        create comment for a given article
        """
        comment_data = request.data.get('comment', {})
        context = {
            'author': request.user.profile
        }
        try:
            context['article'] = Article.objects.get(article_slug=article_slug)
        except Article.DoesNotExist:
            return Response({
                'error': 'Article with that slug not found',
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=comment_data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = {
            'message': 'Comment Added Succesfully',
            'comment': serializer.data
        }
        return Response(message,
                        status=status.HTTP_201_CREATED
                        )

    def list(self, request, article_slug=None):
        """
        return a list of all comments for an article
        """
        try:
            article = Article.objects.get(article_slug=article_slug)
        except Article.DoesNotExist:
            return Response({
                'error': 'Article with this slug not found'
            }, status=status.HTTP_404_NOT_FOUND)
        filters = {
            self.lookup_field: self.kwargs[self.lookup_url_kwarg]
        }
        comments = self.queryset.filter(**filters)
        serializer = CommentSerializer(comments, many=True)
        data = serializer.data
        return Response({
            'comments': data,
            'commentsCount': len(data)
        }, status=status.HTTP_200_OK) if len(data) else \
            Response({
                'message': 'No comments found for this article'
            })


class UpdateDestroyCommentsAPIView(DestroyAPIView, UpdateAPIView):
    """
    delete or update comment by comment id
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.all()
    lookup_url_kwarg = 'comment_pk'
    serializer_class = CommentSerializer

    def destroy(self, request, article_slug=None, comment_pk=None):
        """
        delete comment with comment_id of article with specified slug
        """
        try:
            comment = Comment.objects.get(pk=comment_pk)
            article = Article.objects.get(article_slug=article_slug)
        except Comment.DoesNotExist:
            return Response({
                'error': 'Comment with that ID not found',
            }, status=status.HTTP_404_NOT_FOUND)
        except Article.DoesNotExist:
            return Response({
                'error': 'Article with that slug not found',
            }, status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response({
            'message': 'Comment deleted successfully',
        }, status=status.HTTP_200_OK)

    def update(self, request, article_slug=None, comment_pk=None):
        """
        update comment with comment_id or artcle_slug
        """
        comment_data = request.data.get('comment', {})
        try:
            article = Article.objects.get(article_slug=article_slug)
            comment = Comment.objects.get(pk=comment_pk)
        except Article.DoesNotExist:
            return Response({
                'error': 'Article with this slug not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Comment.DoesNotExist:
            return Response({
                'error': 'Comment with this ID not found'
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(instance=comment, data=comment_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Comment Updated Successfully',
            'comment': serializer.data
        }, status=status.HTTP_200_OK)


class ReplyListAPIView(ListCreateAPIView):
    """
    class to create and list comments replies
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ReplySerializer
    queryset = Reply.objects.select_related(
        'comment', 'author', 'comment__article__author__profile'
    )

    def list(self, request, article_slug=None, comment_pk=None):
        """
        list replies for comment_id
        """
        try:
            Article.objects.get(article_slug=article_slug)
            Comment.objects.get(pk=comment_pk)
        except Article.DoesNotExist:
            return Response({
                'error': 'Article with this slug not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Comment.DoesNotExist:
            return Response({
                'error': 'Comment with this ID not found'
            }, status=status.HTTP_404_NOT_FOUND)
        replies = self.queryset.filter(comment__id=comment_pk)
        serializer = ReplySerializer(replies, many=True)
        data = serializer.data
        return Response({
            'replies': data,
            'repliesCount': len(data)
        }, status=status.HTTP_200_OK) if len(data) else \
            Response({
                'message': 'No replies found for this comment'
            })

    def create(self, request, article_slug=None, comment_pk=None):
        """
        reply to a comment on article with article_slug
        """
        reply_data = request.data.get('reply', {})
        context = {
            'author': request.user.profile
        }
        try:
            Article.objects.get(article_slug=article_slug)
            context['comment'] = Comment.objects.get(pk=comment_pk)
        except Article.DoesNotExist:
            return Response({
                'error': 'Article with that slug not found',
            }, status=status.HTTP_404_NOT_FOUND)
        except Comment.DoesNotExist:
            return Response({
                'error': 'Comment with that ID does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=reply_data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = {
            'message': 'Reply Added Succesfully',
            'reply': serializer.data
        }
        return Response(message,
                        status=status.HTTP_201_CREATED
                        )


class UpdateDestroyReplyAPIView(DestroyAPIView, UpdateAPIView):
    """
    delete a comment's reply or update a reply
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Reply.objects.all()
    lookup_url_kwarg = 'reply_pk'
    serializer_class = CommentSerializer
    NO_COMMENT_ID = Response({
        'error': 'Comment with that ID not found',
    }, status=status.HTTP_404_NOT_FOUND)
    NO_ARTICLE_SLUG = Response({
        'error': 'Article with that slug not found',
    }, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, article_slug=None, comment_pk=None, reply_pk=None):
        """
        delete comment with comment_id of article with specified slug
        """
        try:
            Comment.objects.get(pk=comment_pk)
            Article.objects.get(article_slug=article_slug)
            reply = Reply.objects.get(pk=reply_pk)
        except Comment.DoesNotExist:
            return self.NO_COMMENT_ID
        except Article.DoesNotExist:
            return self.NO_ARTICLE_SLUG
        except Reply.DoesNotExist:
            return Response({
                'error': 'Reply with that ID not found',
            }, status=status.HTTP_404_NOT_FOUND)
        reply.delete()
        return Response({
            'message': 'Reply deleted successfully',
        }, status=status.HTTP_200_OK)

    def update(self, request, article_slug=None, comment_pk=None, reply_pk=None):
        """
        update comment with comment_id or artcle_slug
        """
        reply_data = request.data.get('reply', {})
        try:
            Article.objects.get(article_slug=article_slug)
            Comment.objects.get(pk=comment_pk)
            reply = Reply.objects.get(pk=reply_pk)
        except Article.DoesNotExist:
            return self.NO_ARTICLE_SLUG
        except Comment.DoesNotExist:
            return self.NO_COMMENT_ID
        except Reply.DoesNotExist:
            return Response({
                'error': 'Reply with that ID not found',
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = ReplySerializer(instance=reply, data=reply_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Reply Updated Successfully',
            'reply': serializer.data
        }, status=status.HTTP_200_OK)


# Create your views here.


class RatingsAPIView(APIView):
    """The ratings view for handling http requests"""
    serializer_class = RatingSerializer

    def post(self, request, **kwargs):
        slug = kwargs.get("slug", '')
        article = Article.objects.filter(article_slug=slug).first()
        response = ""
        returned = [Response(dict(
            errors=dict(
                message="The article with slug %s does not exist" %
                        slug)), status=status.HTTP_404_NOT_FOUND), None][article is not None]
        valid_user = request.user
        # valid_user = User.objects.get(email=user.get('email', 'not_there'))
        # First check if the token is really having an associated
        # user. Because sometimes an account might be deactivated or deleted
        # before the token expires which might cause the application to save
        # a rating for an Invalid user
        rating = request.data.get('rating', None)
        # In-case the user never provided the rating in the request
        # throw an error
        returned = [Response(dict(errors=dict(
            message="Missing rating field"
        )), status=status.HTTP_400_BAD_REQUEST), None][rating is not None]
        rating = str(rating)
        try:
            rating = int(float(rating))
        except ValueError:
            rating = 0
        if not 1 <= rating <= 5:
            response = [dict(errors=
                             dict(rating="Specify a valid rating between 1 and 5 inclusive")),
                        response][response != '']
            returned = [Response(response, status=status.HTTP_400_BAD_REQUEST), returned][returned is not None]

        # Check if what was sent by the user is really a number
        # if the number if None
        try:
            if returned is None:
                obje, created = Rating.objects.update_or_create(user=valid_user,
                                                                article=article,
                                                                defaults={"value": rating,
                                                                          'user_id': valid_user.id,
                                                                          'article_id': article.id})
                obje.save()
                response = dict(article={"message": "You successfully rated the article %s %d/5!"
                                                    % (article.title, obje.value)})
                returned = Response(response, status=status.HTTP_201_CREATED)
        except Error:
            response = dict(errors={"message": "There was a problem sending the rating"
                                               " try again later."})
            returned = [Response(response, status=status.HTTP_503_SERVICE_UNAVAILABLE),
                        returned][returned is not None]
        return returned
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
        article.like.add(user.id)
        message = {"article": "You have liked this article"}
        return Response(message, status.HTTP_200_OK)


class DislikeArticle(UpdateAPIView):
    """Class for disliking and  un-disliking an article"""
    def update(self, request, slug):
        """This method updates the liking of an article"""
        LikeArticle.update(self, request, slug)
        article = Article.objects.filter(article_slug=slug).first()
        if article is None:
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
        article.dislike.add(user.id)
        message = {"article": "You have disliked this article"}
        return Response(message, status.HTTP_200_OK)
