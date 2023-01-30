from django.urls import path
from . import views


urlpatterns = [
    path('users/', views.user_list, name = 'user-list'),
    path('users/<int:pk>/', views.user_detail, name = 'user-detail'),
    path('home/', views.musicpost_list, name='get-all-posts'),
    path('<str:username>/', views.get_music_posts_one_user, name='feed'),
    
    
]





