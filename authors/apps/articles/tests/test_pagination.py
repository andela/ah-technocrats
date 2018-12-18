from django.urls import reverse
from rest_framework import status
from .base_test import BaseTestCase


url = 'articles/'
class TestPagination(BaseTestCase):
    """Test class for getting articles"""

    def post_many_articles(self):
        """
        Post more than 10 articles since the page size is 10.
        """
        count = 0
        while count < 15:
            self.create_article()
            count += 1
        return count

    def test_count_of_articles(self):
        """
        Test getting all articles when only one has been posted.
        """
        self.create_article()
        response = self.client.get(self.articles_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        # confirm only the first page has data
        self.assertEqual(response.data['next'], None)
        self.assertEqual(response.data['previous'], None)

    def test_get_many_articles_displays_in_pages(self):
        """
        Test retrieving more than 10 articles displays 10 at a time.
        """
        self.post_many_articles()
        response = self.client.get(self.articles_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 15)
        self.assertEqual(response.data['next'], 'http://testserver/api/articles/?limit=10&offset=10')
        self.assertEqual(response.data['previous'], None)
        