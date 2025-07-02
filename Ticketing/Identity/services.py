from rest_framework_simplejwt.exceptions import AuthenticationFailed

from Ticketing.Identity.exceptions import BadRequest
from .models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group


@transaction.atomic
def signup(data):
    email = data['email']
    existing = User.objects.filter(email=email).first()

    if existing:
        if not existing.is_verified:
            existing.delete()
        else:
            raise BadRequest(f"User with email {email} already exists.")

    user = User.objects.create_user(
        email=email,
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        is_verified=False
    )
    default_group = Group.objects.get(name='USER')
    user.groups.add(default_group)
    return user


def signin(data):
    email = data['email']
    user = User.objects.filter(email=email).first()

    if user:
        if not user.is_verified:
            raise BadRequest(f"Email {email} is not verified.")
        if user is None:
            raise AuthenticationFailed(f"User with email {email} does not exist.")
    return user


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def verify_user_by_email(email: str):
    user = User.objects.filter(email=email).first()
    if not user:
        raise ValidationError(f"User with email {email} does not exist.")
    if user.is_verified:
        raise ValidationError(f"User with email {email} is already verified.")

    user.is_verified = True
    user.save()
    return user

def get_user_list():
    return User.objects.all()
