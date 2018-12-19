from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from authors.apps.articles.models import Comment, Article
from authors.apps.articles.serializers import CommentSerializer
from authors.apps.notifications.models import favorites_notification


@receiver(post_save, sender=Comment)
def notify_favorites(sender, instance, created, **kwargs):
    """
    send a message notification upon commenting on an article.
    """
    if created:
        msg = instance.body
        # print(msg)
        favorites_notification(instance.author, msg, instance)


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
        start = comment_data.get('start', -1)
        end = comment_data.get('end', -1)
        response = None
        try:
            start = int(start)
            end = int(end)
        except ValueError:
            end = -1
            start = 0
            response = Response(dict(errors=dict(
                range="Invalid data for start or selection. They must both be numbers"
            )), status=status.HTTP_400_BAD_REQUEST)
        # The chunk of text that the user has selected
        range_selected = [point for point in [start, end] if point > -1]
        # At this point we assume that the user's highlight is in the
        # correct range between 0 and length of the article body
        context = {
            'author': request.user.profile
        }
        try:
            context['article'] = Article.objects.get(article_slug=article_slug)
        except Article.DoesNotExist:
            return Response({
                'error': 'Article with that slug not found',
            }, status=status.HTTP_404_NOT_FOUND)
        # In case the range is invalid just
        # raise an error
        response = [None, Response(
            dict(errors=dict(
                range="The start of the highlight must be less than or equal"
                      " to "
                      "than the end of highlight")),
            status=status.HTTP_400_BAD_REQUEST)][start > end]
        response = [response, Response(dict(errors=dict(
            range="Please provide both the start and the end or non of them "
                  "they must also be greater than 0"
        )), status=status.HTTP_400_BAD_REQUEST)][
            (len(range_selected) == 1) and response is None]
        CommentsListAPIView.assign_range(response, context, start, end, range_selected)
        article_len = len(context['article'].body)
        response = [response, CommentsListAPIView.check_out_of_range(
            response, start, end, article_len)][response is None]
        response = self.save(
            response,
            comment_data,
            context, [start, end, range_selected]) if response is None else response
        return response

    def list(self, request, article_slug=None):
        """
        return a list of all comments for an article
        """
        article = Article.objects.filter(article_slug=article_slug).first()
        if article is None:
            return Response({
                'error': 'Article with this slug not found'
            }, status=status.HTTP_404_NOT_FOUND)
        filters = {
            self.lookup_field: self.kwargs[self.lookup_url_kwarg]
        }
        comments = self.queryset.filter(**filters)
        whole, sections = CommentsListAPIView.groups(comments, article)
        total_len = len(whole) + len(sections)
        return Response({
            'comments': whole,
            'highlights': sections,
            'commentsCount': total_len
        }, status=status.HTTP_200_OK) if total_len else \
            Response({
                'message': 'No comments found for this article'
            })

    @staticmethod
    def groups(comments, article):
        """Group the comments into highlights and full article comment"""
        sections = []
        whole = []
        for comment in comments:
            if all([comment.highlight_start == 0, comment.highlight_end == -1]):
                whole.append(CommentSerializer(comment).data)
                continue
            one = CommentSerializer(comment).data
            ranges = {"highlight_start": comment.highlight_start}
            ranges.update({"highlight_end": comment.highlight_end})
            one.update({"selection": {"range": ranges,
                                      "text": article.body[comment.highlight_start:comment.highlight_end + 1]}})
            sections.append(one)
        return whole, sections

    @staticmethod
    def check_out_of_range(current_response, start, end, article_len):
        response = None
        if max(start, end) >= article_len:
            response = [current_response, Response(dict(errors=dict(
                range="Bad selection. "
                      "The start and end of selection must "
                      "be between 0 and %d inclusive" % (article_len - 1)
            )), status=status.HTTP_400_BAD_REQUEST)][current_response is None]
        return response

    @staticmethod
    def assign_range(response, context, start, end, range_selected):
        if response is None:
            context['start'] = [0, start][start > -1]
            context['end'] = [-1, end][end > -1]
            return
        if len(range_selected) == 0:
            context['start'] = 0
            context['end'] = -1

    def save(self, response, comment_data, context, ranges):
        """Try to save a comment to the database"""
        try:
            serializer = self.serializer_class(data=comment_data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            current = serializer.data
            current.update({
                               "highlight_start": ranges[0],
                               "highlight_end": ranges[1]} if len(ranges[2]) == 2 else {
            })
            message = {
                'message': 'Comment Added Succesfully',
                'comment': current
            }
            response = Response(message, status=status.HTTP_201_CREATED)

        except Exception as ex:
            response = [response, Response(dict(errors=dict(
                message="Something went wrong please Try again later"
            )), status=status.HTTP_400_BAD_REQUEST)][response is None]
        return response


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

