from django.urls import path
from app.views import explore_views as views






urlpatterns = [
    path('', views.explore_posts, name='get-all-posts'),
    path('<int:pk>/likes', views.change_likes_count, name='change-likes-count')

]


