from django.urls import path
from app.views import login_views as views
# from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.login_user, name='login'),
]
