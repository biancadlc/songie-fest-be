from django.urls import path
from app.views import music_post_views as views




urlpatterns = [
    path('<int:pk>/', views.music_post_details, name='music-post-detail'),
    path('<int:pk>/comments/', views.comment_list, name='comment-list'),
    path('<int:pk>/comments/<int:id>/', views.delete_comment, name='delete_comment'),
    path('get-username/<int:commentid>', views.get_username, name='get_username')

]

