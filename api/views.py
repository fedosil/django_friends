from django.http import Http404
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        message = User.objects.get(pk=request.user.id).status(obj.id)
        return Response({'message': message}, status=status.HTTP_200_OK)


class FriendsListCreate(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.get(pk=self.request.user.id).get_friends()

    def create(self, request, *args, **kwargs):
        try:
            user_id = request.data['user_id']
            try:
                obj = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                raise Http404
            if request.user.id == obj.id:
                return Response({'message': 'it is impossible to subscribe to yourself'}, status=status.HTTP_400_BAD_REQUEST)
            message = User.objects.get(pk=request.user.id).follow(obj.id)
            if message:
                return Response({'message': message}, status=status.HTTP_200_OK)
            Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except KeyError:
            return Response({'user_id': 'This field is required'}, status=status.HTTP_400_BAD_REQUEST)

class FRequestsList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.get(pk=self.request.user.id).get_requests()


class FollowersList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.get(pk=self.request.user.id).get_followers()
