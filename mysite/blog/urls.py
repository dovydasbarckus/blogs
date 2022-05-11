

from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('articles/', views.ArticlesListView.as_view(), name='articles'),
    path('articles/create', views.ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>', views.ArticleDetailView.as_view(), name='article_detail'),
    path('my_articles/', views.MyArticlesListView.as_view(), name='my_articles'),
    path('my_articles/<int:pk>', views.MyArticleDetailView.as_view(), name='my_articles_detail'),
    path('my_articles/<int:pk>/update', views.ArticleUpdateView.as_view(), name='article-update'),
    path('my_articles/<int:pk>/delete', views.ArticleDeleteView.as_view(), name='article-delete'),
    path('comment/<int:pk>', views.ArticleCommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete', views.ArticleCommentDeleteView.as_view(), name='comment_delete'),
]