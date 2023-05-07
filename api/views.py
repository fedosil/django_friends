from rest_framework import generics
from rest_framework import permissions

from users.models import User
from users.serializers import UserSerializer, UserDetailSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

class FriendsList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = super(FriendsList, self).get_queryset()
        return queryset.get(pk=self.request.user.id).friends.all()

class FRequestsList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = super(FRequestsList, self).get_queryset()
        return queryset.get(pk=self.request.user.id).f_requests.all()

class FollowersList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = super(FollowersList, self).get_queryset()
        return queryset.filter(f_requests=self.request.user)

