from django.urls import path

from .views import ArticleAPIView, SpecificArticleAPIView

urlpatterns = [
    path('articles/', ArticleAPIView.as_view(), name='articles'),
    path('articles/<slug>', SpecificArticleAPIView.as_view(), name='get_article')
]