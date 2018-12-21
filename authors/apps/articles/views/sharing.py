from django.urls import reverse
from django_social_share.templatetags import social_share
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.apps.articles.models import Article


class ShareArticleAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # This view returns the link to share articles. The parameters we get
        # from the url, retrieve the article and generate the url for sharing.
        share_to = kwargs['share_to']
        slug = kwargs['slug']
        article = Article.objects.filter(article_slug=slug).first()
        if article is None:
            return Response({"Error": "Article not found"}, status.HTTP_404_NOT_FOUND)
        article_link = request.build_absolute_uri(
            reverse('articles:get_article', kwargs={'slug': article.article_slug})
            )
        context = {'request': request}
        text = "Read this article on Authors Haven"
        subject = "New Article on Authors Haven: {}".format(article.title)
        if share_to == 'email':
            link = social_share.send_email_url(context, subject, text, article_link)['mailto_url']
            return Response(link, status=status.HTTP_200_OK)
        return Response(self.set_link(context, share_to, article_link, args), status.HTTP_200_OK)

    def set_link(self, context, share_to, article_link, *args):
        providers = {
            "twitter": [social_share.post_to_twitter_url, "tweet_url"],
            "facebook": [social_share.post_to_facebook_url, "facebook_url"],
            "reddit": [social_share.post_to_reddit_url, "reddit_url"],
            "gplus": [social_share.post_to_gplus_url, "gplus_url"]
            }
        provider_link = providers.get(share_to, providers['facebook'])
        return provider_link[0](context, article_link)[provider_link[1]]
