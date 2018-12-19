from django.db import Error
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.apps.articles.models import Article, Rating
from authors.apps.articles.serializers import RatingSerializer


class RatingsAPIView(APIView):
    """The ratings view for handling http requests"""
    serializer_class = RatingSerializer

    def post(self, request, **kwargs):
        slug = kwargs.get("slug", '')
        article = Article.objects.filter(article_slug=slug).first()
        response = ""
        returned = [Response(dict(
            errors=dict(
                message="The article with slug %s does not exist" %
                        slug)), status=status.HTTP_404_NOT_FOUND), None][article is not None]
        valid_user = request.user
        # valid_user = User.objects.get(email=user.get('email', 'not_there'))
        # First check if the token is really having an associated
        # user. Because sometimes an account might be deactivated or deleted
        # before the token expires which might cause the application to save
        # a rating for an Invalid user
        rating = request.data.get('rating', None)
        # In-case the user never provided the rating in the request
        # throw an error
        returned = [Response(dict(errors=dict(
            message="Missing rating field"
        )), status=status.HTTP_400_BAD_REQUEST), None][rating is not None]
        rating = str(rating)
        try:
            rating = int(float(rating))
        except ValueError:
            rating = 0
        if not 1 <= rating <= 5:
            response = [dict(errors=
                             dict(rating="Specify a valid rating between 1 and 5 inclusive")),
                        response][response != '']
            returned = [Response(response, status=status.HTTP_400_BAD_REQUEST), returned][returned is not None]

        # Check if what was sent by the user is really a number
        # if the number if None
        try:
            if returned is None:
                obje, created = Rating.objects.update_or_create(user=valid_user,
                                                                article=article,
                                                                defaults={"value": rating,
                                                                          'user_id': valid_user.id,
                                                                          'article_id': article.id})
                obje.save()
                response = dict(article={"message": "You successfully rated the article %s %d/5!"
                                                    % (article.title, obje.value)})
                returned = Response(response, status=status.HTTP_201_CREATED)
        except Error:
            response = dict(errors={"message": "There was a problem sending the rating"
                                               " try again later."})
            returned = [Response(response, status=status.HTTP_503_SERVICE_UNAVAILABLE),
                        returned][returned is not None]
        return returned
