from django.urls import path
from app.views import register_views as views
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    
    path('', views.register_view, name='register')
]

