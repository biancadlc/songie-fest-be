"""songiefest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token



# ==== GEEKS FOR GEEKS ====#
urlpatterns = [
    path("admin/", admin.site.urls),
    path('explore/', include('app.urls.explore_urls')),
    path('users/', include('app.urls.users_urls')),
    path('register/', include('app.urls.register_urls')),
    path('music_post/', include('app.urls.music_post_urls')),
    path('<str:username>/', include('app.urls.profile_urls')),

    path('login/', obtain_auth_token, name='login'), 
    # path('login/', include('app.urls.login_urls')),

    path('auth/', obtain_auth_token)
]
