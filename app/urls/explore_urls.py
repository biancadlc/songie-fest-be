from django.urls import path
from app.views import explore_views as views






urlpatterns = [
    path('', views.explore_posts, name='get-all-posts'),
    path('<int:pk>/likes/', views.get_username_likes, name='change-likes-count'),
    path('<int:pk>/likes-count/', views.get_like_count, name='change-likes-count')

]


