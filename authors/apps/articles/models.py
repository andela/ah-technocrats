from django.db import models
from django.utils.text import slugify
import uuid

from ..authentication.models import User

class Article(models.Model):
    """
    Article model class.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=False)
    body = models.TextField()
    image = models.URLField(blank=True)
    # slug is unique to an article
    article_slug = models.SlugField(unique=True, editable=False, max_length=255)
    author = models.ForeignKey(User, related_name='authorshaven', on_delete=models.CASCADE)
    # auto_add_now is updated on creation only
    # auto_now is updated with change
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        """
        Return the article title.
        """
        return self.title

    def create_slug(self):
        """
        Create a unique label for each article.
        """
        slug = slugify(self.title)
        while Article.objects.filter(article_slug=slug).exists():
            slug = slug + '-' + uuid.uuid4().hex
        return slug
    
    def save(self, *args, **kwargs):
        """
        Edit the save function to include the created slug.
        """
        self.article_slug = self.create_slug()
        super().save(*args,**kwargs)
