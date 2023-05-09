from django.http import Http404
from rest_framework import generics, status, mixins
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer


class UserList(generics.ListAPIView):
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


class FriendsListCreateDelete(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get_queryset(self):
        return User.objects.get(pk=self.request.user.id).get_friends()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data['user_id']
            obj = self.get_object(user_id)
            if request.user.id == obj.id:
                return Response({'message': 'it is impossible to subscribe to yourself'},
                                status=status.HTTP_400_BAD_REQUEST)
            message = User.objects.get(pk=request.user.id).follow(obj.id)
            if message:
                return Response({'message': message}, status=status.HTTP_200_OK)
            Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except KeyError:
            return Response({'user_id': 'This field is required'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            user_id = request.data['user_id']
            obj = self.get_object(user_id)
            if request.user.id == obj.id:
                return Response({'message': 'it is impossible to delete yourself'},
                                status=status.HTTP_400_BAD_REQUEST)
            message = User.objects.get(pk=request.user.id).f_delete(obj.id)
            if message:
                return Response({'message': message}, status=status.HTTP_200_OK)
            Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except KeyError:
            return Response({'user_id': 'This field is required'}, status=status.HTTP_400_BAD_REQUEST)

class FRequestsList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.get(pk=self.request.user.id).get_requests()


class FollowersList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.get(pk=self.request.user.id).get_followers()
