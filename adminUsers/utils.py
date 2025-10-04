# utils.py
import datetime
import jwt
from django.conf import settings
from .models import UserToken
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

def generate_jwt_for_superuser(user, response):
    """
    Generate JWT for superuser, save in DB, and set in cookies.
    """
    if not user.is_superuser:
        return None  # Only superusers get JWT

    payload = {
        "user_id": user.id,
        "username": user.username,
        "is_superuser": user.is_superuser,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # expires in 1 hour
        "iat": datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    # Save in DB
    UserToken.objects.update_or_create(user=user, token=token)

    # Set cookie (HttpOnly for security)
    response.set_cookie(
        key="jwt",
        value=token,
        httponly=True,
        secure=False,  # change to True in production with HTTPS
        samesite="Strict"
    )

    return token



def checkUserIsAuthenticated(request):
    token = request.COOKIES.get("jwt")
    if not token:
        return False
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
        if not UserToken.objects.filter(user_id=payload["user_id"], token=token).exists():
            return False
        return True
    except ExpiredSignatureError:
        return False
    except InvalidTokenError:
        return False
    
