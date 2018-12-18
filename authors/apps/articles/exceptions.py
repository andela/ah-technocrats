from rest_framework.exceptions import NotFound

class ArticleNotFound(NotFound):
    default_detail = 'Article with this slug not found'