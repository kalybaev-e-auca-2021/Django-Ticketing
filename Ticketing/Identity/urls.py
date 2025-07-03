from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from Ticketing.Identity.views import SignUpView, SignInView, VerifyView, AssignRoleView, ListUsersView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/signin/', SignInView.as_view(), name='signin'),
    path('auth/verify/', VerifyView.as_view(), name='verify'),
    path('auth/assign-role/', AssignRoleView.as_view(), name='assign-role'),
    path('auth/users/', ListUsersView.as_view(), name='list-users'),
]
