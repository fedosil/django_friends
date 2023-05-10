from rest_framework import serializers

from users.models import User

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
        read_only_fields = ('id', 'username')


class UserResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

class UserRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
