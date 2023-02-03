from django.urls import path
from app.views import profile_views as views
from rest_framework.authtoken.views import obtain_auth_token




urlpatterns = [
    
    path('', views.profile_view, name='profile'),
    path('account/', views.account_details, name='account'),


]

