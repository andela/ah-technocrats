import uuid
from django.db import models
from django.utils.text import slugify

from ..authentication.models import User
from authors.apps.profiles.models import Profile

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

class Comment(models.Model):
    """
    comment model
    """
    body = models.TextField(
        max_length=1000,
        blank=False,
        null=False,
    )
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        """"
        order comments chronologically by date created and last update"""
        ordering = ['-created_at', '-last_update']
    
    def __str__(self):
        """
        return comment body
        """
        return self.body

class Reply(models.Model):
    """
    comment reply model
    """
    author = models.ForeignKey(Profile, related_name='reply', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment, related_name='reply', on_delete=models.CASCADE)
    body = models.TextField(
        null=False,
        blank=False,
    )

    def __str__(self):
        """
        return reply body
        """
        return self.body
    
    class Meta:
        """
        order replies chronologically by creation date
        """
        ordering = ['-created_at']
