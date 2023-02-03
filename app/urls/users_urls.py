from django.urls import path
from app.views import users_views as views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.user_list, name='user-list'),
]

