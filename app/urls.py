from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token





urlpatterns = [
    
    path('register/', views.registration_view, name = 'register'),
    path('login/', obtain_auth_token, name = 'login'), #log in only works with superusers
    path('users/', views.user_list, name = 'user-list'),
    path('users/<int:pk>/', views.account_details, name = 'account-details'),
    path('home/', views.musicpost_list, name='get-all-posts'),

    path('<str:username>/', views.profile_view, name='profile'),

    
    path('musicpost/<int:pk>/', views.musicpost_detail, name='music-post-detail'),
    path('musicpost/<int:pk>/comments/', views.comment_list, name='comment-list'),
    path('musicpost/<int:pk>/comments/<int:id>/', views.delete_comment, name='delete_comment'),

]




