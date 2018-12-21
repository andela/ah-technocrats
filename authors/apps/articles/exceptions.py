from rest_framework.exceptions import NotFound

class ArticleNotFound(NotFound):
    default_detail = 'Article with this slug not found'
    
class CommentNotFound(NotFound):
    """
    comment id not found exception
    """

    default_detail = 'Comment not found.'
