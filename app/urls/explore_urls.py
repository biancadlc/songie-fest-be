from django.urls import path
from app.views import explore_views as views
from rest_framework.authtoken.views import obtain_auth_token





urlpatterns = [
    path('', views.explore_posts, name='get-all-posts'),

]


