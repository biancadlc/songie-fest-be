from django.urls import path
from . import views


urlpatterns = [
    path('users/', views.user_list, name = 'user-list'),
    path('users/<int:pk>/', views.user_detail, name = 'user-detail'),
    path('home/', views.musicpost_list, name='get-all-posts'),
    # path('<str:username>/', views.get_music_posts_one_user, name='feed'),
    
    path('musicpost/<int:pk>/', views.musicpost_detail, name='music-post-detail'),
    path('musicpost/<int:pk>/comments/', views.comment_list, name='comment-list'),
    # path('musicpost/<int:pk>/likes/', views.like_music_post, name='like-music-post'),
    path('<str:username>/', views.get_music_posts_one_user, name='feed'),
]




