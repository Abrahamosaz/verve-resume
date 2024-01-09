from django.urls import path
from  .views import (SignupView, LoginView, refresh_token,
                     confirm_email, resendConfirm_email, reset_password)

urlpatterns = [
    path("auth/signup", SignupView.as_view(), name="signup"),
    path("auth/login", LoginView.as_view(), name="login"),
    path("token/refresh", refresh_token, name="refresh"),
    path("auth/confirmEmail", confirm_email, name="confirm_email"),
    path("auth/resendConfirmEmail", resendConfirm_email, name="resend_email"),
    path("auth/resetPassword", reset_password, name="reset_password")
]