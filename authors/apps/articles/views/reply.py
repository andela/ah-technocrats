from rest_framework import status
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from authors.apps.articles.models import Reply, Article, Comment
from authors.apps.articles.serializers import ReplySerializer, CommentSerializer


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

