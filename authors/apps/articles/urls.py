from django.urls import path

from authors.apps.articles.views.articles import ArticleAPIView, SpecificArticleAPIView, LikeArticle, DislikeArticle
from authors.apps.articles.views.bookmarks import BookMarkCreateAPIView, BookMarkListAPIView
from authors.apps.articles.views.comments import CommentsListAPIView, UpdateDestroyCommentsAPIView
from authors.apps.articles.views.favorites import FavoriteArticles
from authors.apps.articles.views.ratings import RatingsAPIView
from authors.apps.articles.views.reply import ReplyListAPIView, UpdateDestroyReplyAPIView
from authors.apps.articles.views.report_articles import ReportArticleAPIView, ReportListAPIView
from authors.apps.articles.views.like_dislike_comments import (
    LikeComment,
    DislikeComment,
)
    

urlpatterns = [
    path('articles/', ArticleAPIView.as_view(), name='articles'),
    path('articles/<slug>', SpecificArticleAPIView.as_view(), name='get_article'),
    path('articles/<str:article_slug>/comments/', CommentsListAPIView.as_view(), name='list-create-comment'),
    path('articles/<str:article_slug>/comments/<int:comment_pk>/', UpdateDestroyCommentsAPIView.as_view(), name='update-delete-comment'),
    path('articles/<str:article_slug>/comments/<int:comment_pk>/replies/', ReplyListAPIView.as_view(), name='list-create-reply'),
    path('articles/<str:article_slug>/comments/<int:comment_pk>/replies/<int:reply_pk>/', UpdateDestroyReplyAPIView.as_view(), name='update-delete-reply' ),
    path('articles/<str:slug>/rate/', RatingsAPIView.as_view(), name='rate-article'),
    path('articles/<slug>/like/', LikeArticle.as_view(), name='like'),
    path('articles/<slug>/dislike/', DislikeArticle.as_view(), name='dislike'),
    path('articles/<slug>/favorite/', FavoriteArticles.as_view(), name='favorite'),
    path('articles/<str:slug>/report/', ReportArticleAPIView.as_view(), name='report'),
    path('articles/reports/', ReportListAPIView.as_view(), name='report-list'),
    path('articles/<str:article_slug>/bookmark/', BookMarkCreateAPIView.as_view(), name='bookmark-article'),
    path('articles/bookmarks/', BookMarkListAPIView.as_view(), name='get-bookmarks'),
    path('comments/<int:comment_pk>/like/', LikeComment.as_view(), name='like-comment'),
    path('comments/<int:comment_pk>/dislike/', DislikeComment.as_view(), name='dislike-comment'),
]
