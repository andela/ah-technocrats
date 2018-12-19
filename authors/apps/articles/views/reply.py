from rest_framework import status
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from authors.apps.articles.models import Reply, Article, Comment
from authors.apps.articles.serializers import ReplySerializer, CommentSerializer


class CommentReplyChecker:

    @staticmethod
    def check_exists(comment_pk, article_slug, reply_id=None):
        """Check if a comment or an article or a reply exists"""
        article = Article.objects.filter(article_slug=article_slug).first()
        comment = Comment.objects.filter(pk=comment_pk).first()
        response = [None, Response({
            'error': 'Article with this slug not found'
        }, status=status.HTTP_404_NOT_FOUND)][article is None]
        response = [response, Response({
            'error': 'Comment with this ID not found'
        }, status=status.HTTP_404_NOT_FOUND)][(response is None) and (comment is None)]
        reply = [None, Reply.objects.filter(pk=reply_id).first()][reply_id is not None]
        response = [response, Response({
                'error': 'Reply with that ID not found',
            }, status=status.HTTP_404_NOT_FOUND)][
            (response is None) and (not reply) and (reply_id is not None)]
        if response is not None:
            return response
        return [article, comment, reply]


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
        response = CommentReplyChecker.check_exists(comment_pk, article_slug)
        if not isinstance(response, list):
            return response
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
        resp = CommentReplyChecker.check_exists(comment_pk, article_slug)
        if not isinstance(resp, list):
            return resp
        context['comment'] = resp[1]
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

    def destroy(self, request, article_slug=None, comment_pk=None, reply_pk=None):
        """
        delete comment with comment_id of article with specified slug
        """
        response = CommentReplyChecker.check_exists(comment_pk, article_slug, reply_pk)
        if not isinstance(response, list):
            return response
        reply = response[2]
        reply.delete()
        return Response({
            'message': 'Reply deleted successfully',
        }, status=status.HTTP_200_OK)

    def update(self, request, article_slug=None, comment_pk=None, reply_pk=None):
        """
        update comment with comment_id or artcle_slug
        """
        reply_data = request.data.get('reply', {})
        resp = CommentReplyChecker.check_exists(comment_pk, article_slug, reply_pk)
        if not isinstance(resp, list):
            return resp
        reply = resp[2]
        serializer = ReplySerializer(instance=reply, data=reply_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Reply Updated Successfully',
            'reply': serializer.data
        }, status=status.HTTP_200_OK)
