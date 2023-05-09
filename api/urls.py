from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('users', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('friends', views.FriendsListCreateDelete.as_view()),
    path('requests', views.FRequestsList.as_view()),
    path('followers', views.FollowersList.as_view()),
]
