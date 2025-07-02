from rest_framework import serializers

from Ticketing.Identity.models import User


class SignupRequestSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class VerifyUserSerializer(serializers.Serializer):
    email = serializers.EmailField()

class SigninRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserListSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_verified', 'roles']

    def get_roles(self, obj):
        return [group.name for group in obj.groups.all()]
