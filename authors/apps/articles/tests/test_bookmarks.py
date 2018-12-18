from rest_framework import status
from .base_test import BaseTestCase
from django.urls import reverse
from authors.apps.articles.models import BookMarkArticle

class TestBookMarks(BaseTestCase):
    """
    test bookmarking article functionality
    """

    def test_get_empty_bookmarks(self):
        """
        test getting bookmarks when none exisits
        """
        # article_url, slug_1, token = self.create_article()
        self.user_signup()
        token = self.user_login()
        response = self.client.get(
            self.bookmarks_url,
            format='json',
            HTTP_AUTHORIZATION='Token '+ token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'No articles bookmarked yet.')
        self.assertFalse(
            BookMarkArticle.objects.all()
        ) # confirm no bookmarks in model
        

    def test_toogle_bookmarking_article(self):
        """
        test bookmarking existing article slug
        """
        article_url, response, token = self.create_article()
        article_slug1= response.data['slug']
        respons = self.toogle_bookmarking_article(article_slug1, token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(BookMarkArticle.objects.all())
        self.assertEqual(respons.data['message'], 'Article bookmarked successfully')
        response2 = self.toogle_bookmarking_article(article_slug1, token)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data['message'], 'Bookmark deleted successfully')
        self.assertFalse(
            BookMarkArticle.objects.all()
        ) # confirm no bookmarks in model

    def test_bookmarking_non_exisiting_slug(self):
        """
        test bookmarking a non exisiting article
        """
        self.user_signup()
        token = self.user_login()
        article_slug = 'non-existing-article'
        response = self.toogle_bookmarking_article(
            article_slug,
            'Token '+ token
        )
        self.assertEqual(response.data['detail'],'Article with this slug not found')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
