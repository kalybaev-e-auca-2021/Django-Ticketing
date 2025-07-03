from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import User
from .serializers import SignupRequestSerializer, VerifyUserSerializer, SigninRequestSerializer, UserListSerializer
from .services import signup, verify_user_by_email, signin, get_tokens_for_user, get_user_list


class SignUpView(APIView):
    def post(self, request):
        serializer = SignupRequestSerializer(data=request.data)
        if serializer.is_valid():
            signup(serializer.validated_data)
            return Response({"message": "Please verify your email"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    def post(self, request):
        serializer = SigninRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = signin(serializer.validated_data)

            if not user.check_password(serializer.validated_data['password']):
                raise AuthenticationFailed("Invalid credentials")

            tokens = get_tokens_for_user(user)

            return Response({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "authToken": tokens['access'],
                "roles": [group.name for group in user.groups.all()]
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyView(APIView):
    def post(self, request):
        serializer = VerifyUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = verify_user_by_email(serializer.validated_data['email'])
                return Response({'message': f'User {user.email} verified successfully.'})
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignRoleView(APIView):
    @permission_classes([IsAuthenticated])
    def post(self, request):
        email = request.data.get('email')
        role = request.data.get('role')

        if role not in ['ADMIN', 'USER']:
            return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)

        return Response({'message': f"Role '{role}' assigned to user {email}."})


class ListUsersView(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
