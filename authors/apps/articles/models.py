import uuid

from django.db import models
from django.utils.text import slugify

from authors.apps.profiles.models import Profile
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
    # add like and dislike field in the articles
    like = models.ManyToManyField(User, blank=True, related_name='like')
    dislike = models.ManyToManyField(User, blank=True, related_name='dislike')

    favorite = models.ManyToManyField(User, blank=True, related_name='favorite')

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
        super().save(*args, **kwargs)

    @property
    def rating(self):
        """Get the average rating of an article
        including the distribution of the ratings"""
        rated = Rating.objects.filter(article=self)
        distributions = dict()
        total = 0
        for ratee in rated:
            distributions[ratee.value] = distributions.setdefault(ratee.value, 0) + 1
            total += ratee.value
        counts = 1
        if len(rated) > 0:
            counts = len(rated)
        rate = round(total / counts, 1)
        individuals = distributions
        average = {'average': rate}
        final = dict()
        final.update(average)
        final.update({"distributions": individuals})
        return final

    @property
    def just_average(self):
        """Return just the average ratings without distributions"""
        return self.rating.get('average')


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
    # The beginning of the highlight
    highlight_start = models.IntegerField(default=0)
    # The end of the highlight
    highlight_end = models.IntegerField(default=-1)
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


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    value = models.IntegerField(choices=zip(range(1, 6), (1, 6)))

    class Meta:
        db_table = "ratings"
        # Create a unique key which is a combination of
        # two fields
        unique_together = ("article", "user")


class ReportArticle(models.Model):
    class Meta:
        verbose_name = "Reported Article"
        verbose_name_plural = "Reported Articles"

    REPORT_CHOICES = (
        (0, 'None'),
        (1, 'Incites Violence'),
        (2, 'Duplicate content'),
        (3, 'Indecent Content'),
        (4, 'Poorly Written')
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.IntegerField(blank=False, null=False, choices=REPORT_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def show_report(self):
        choice = int(self.report)
        return self.REPORT_CHOICES[choice]

    def __str__(self):
        user = self.reported_by
        report = self.show_report()
        article = self.article.title
        return """Article Titled: "{}" was reported By User: {} for Report: {}""".format(article, user, report)


class BookMarkArticle(models.Model):
    """
    model for holding users bookmarks. Allow user to bookmark an article only once
    """
    class Meta:
        """
        allow user to bookmark an article only once
        """
        unique_together = ('article', 'user')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user', related_name='user')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='article', related_name='article')

    def __str__(self):
        """
        return the name of the bookmarked article
        """
        return self.article.article_slug
