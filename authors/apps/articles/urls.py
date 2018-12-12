from django.urls import path

from .views import ArticleAPIView, SpecificArticleAPIView, CommentsListAPIView, \
    UpdateDestroyCommentsAPIView, ReplyListAPIView, \
    UpdateDestroyReplyAPIView



urlpatterns = [
    path('articles/', ArticleAPIView.as_view(), name='articles'),
    path('articles/<slug>', SpecificArticleAPIView.as_view(), name='get_article'),
    path('articles/<str:article_slug>/comments/', CommentsListAPIView.as_view(), name='list-add-comment'),
    path('articles/<str:article_slug>/comments/<int:comment_pk>/', UpdateDestroyCommentsAPIView.as_view(), name='update-delete-comment'),
    path('articles/<str:article_slug>/comments/<int:comment_pk>/replies/', ReplyListAPIView.as_view(), name='list-create-reply'),
    path('articles/<str:article_slug>/comments/<int:comment_pk>/replies/<int:reply_pk>/', UpdateDestroyReplyAPIView.as_view(), name='update-delete-reply' ),
]
