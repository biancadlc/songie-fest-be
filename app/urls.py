from django.urls import path
from . import views

# urlpatterns = [
#     path('', views.AppOverview, name='home'),
#     path('create/', views.add_user, name='add-user'),
#     path('all/', views.view_users, name='view_users'),
#     path('update/<int:pk>/', views.update_users, name='update-users'),
    
    
# ]

# ===== GEEKS TUTORIAL ==== #

urlpatterns = [
    path('users/',
        views.user_list,
        name = 'user-list'),
    path('users/<int:pk>/',
        views.user_detail,
        name = 'user-detail'),
]


