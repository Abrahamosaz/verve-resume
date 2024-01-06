from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings


User = get_user_model()



def create_access_refresh_jwt_token(user, life_time=None):
    refresh = RefreshToken.for_user(user)
    if life_time:
        refresh.lifetime = life_time
    return refresh



def jwt_payload_handler(user: User):
    payload = {
        "id": user.id,
        "email": user.email
    }
    return payload


def create_jwt_token(user: User):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token
    

