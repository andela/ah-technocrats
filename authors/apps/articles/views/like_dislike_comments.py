from rest_framework.generics import UpdateAPIView
from authors.apps.articles.models import Comment
from rest_framework.response import Response
from rest_framework import status
from authors.apps.articles.exceptions import CommentNotFound

class LikeComment(UpdateAPIView):
    """Class for liking and un-liking an article"""

    def update(self, request, comment_pk):
        """This method updates the liking of an article"""
        try:
            comment = Comment.objects.get(id=comment_pk)
        except Comment.DoesNotExist:
            raise CommentNotFound

        # gets the user of that specific session
        user = request.user
        # checks for the boolean value of liking an comments
        liked = bool(user in comment.likes.all())
        if liked is True:
            comment.likes.remove(user.id)
            message = {"message": "You have unliked this comment"}
            return Response(message, status.HTTP_200_OK)

        # if like is false, the comment is liked
        disliked = bool(user in comment.dislikes.all())
        if disliked is True:
            comment.dislikes.remove(user.id) # un-dislike if user had disliked
        comment.likes.add(user.id) # now like the comment
        message = {"message": "You have liked this comment"}
        return Response(message, status.HTTP_200_OK)


class DislikeComment(UpdateAPIView):
    """Class for disliking and  un-disliking an comment"""

    def update(self, request, comment_pk):
        """This method updates the liking of an comment"""
        comment = Comment.objects.filter(id=comment_pk).first()
        if comment is None:
            raise CommentNotFound

        # gets the user of that specific session
        user = request.user
        # checks for the boolean value of disliking an comment
        disliked = bool(user in comment.dislikes.all())
        if disliked is True:
            comment.dislikes.remove(user.id)
            message = {"message": "This comment has been un-disliked"}
            return Response(message, status.HTTP_200_OK)

        # if dislike is false, the comment is disliked
        liked = bool(user in comment.likes.all())
        if liked is True:
            comment.likes.remove(user.id) # unlike if user had liked
        comment.dislikes.add(user.id) # now dislike the comment
        message = {"message": "You have disliked this comment"}
        return Response(message, status.HTTP_200_OK)
