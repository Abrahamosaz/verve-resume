from django.urls import path, include
from  .views import SignUp, getUser
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("signup",  SignUp.as_view(), name='signup'),
    path("users", getUser.as_view(), name='users'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]