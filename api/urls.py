from django.urls import path, include
from rest_framework import routers

from api import views

app_name = 'api'
router = routers.DefaultRouter()
router.register(r'friends', views.FriendsViewSet)
urlpatterns = [
    path('users', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('requests', views.FRequestsList.as_view()),
    path('followers', views.FollowersList.as_view()),
    path('', include(router.urls)),
]
