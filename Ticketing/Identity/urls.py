from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from Ticketing.Identity.views import signup_view, signin_view, verify_view, assign_role_view, list_users_view

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/signup/', signup_view),
    path('auth/signin/', signin_view),
    path('auth/verify/', verify_view),
    path('auth/assign-role/', assign_role_view),
    path('auth/users/', list_users_view),
]
