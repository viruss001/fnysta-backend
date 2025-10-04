# views.py
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .utils import generate_jwt_for_superuser
import jwt
from django.conf import settings
from rest_framework.decorators import permission_classes, authentication_classes


from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from .models import UserToken

class LoginView(APIView):
    """
    Login API endpoint
    """

    permission_classes = [AllowAny]
    authentication_classes = []  # 🚀 disables SessionAuthentication (no CSRF required)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=401)

        login(request, user)

        response = Response({"message": "Login successful"})

        if user.is_superuser:
            generate_jwt_for_superuser(user, response)
            
            

        return response
    

@api_view(["GET"])
@permission_classes([AllowAny])        # anyone can call, but JWT decides access
@authentication_classes([])            # no CSRF/session checks
def checkUser(request):
    """
    Validate JWT from cookies and return user info.
    """
    token = request.COOKIES.get("jwt")

    if not token:
        return Response({"error": "Not Logged in"}, status=401)

    try:
        # Decode JWT
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        # Optional: verify token exists in DB (extra safety)
        if not UserToken.objects.filter(user_id=payload["user_id"], token=token).exists():
            return Response({"error": "Token not recognized"}, status=401)

        return Response({
            "user_id": payload["user_id"],
            "username": payload["username"],
            "is_superuser": payload["is_superuser"],
            "valid": True
        })

    except ExpiredSignatureError:
        return Response({"error": "Token expired"}, status=401)
    except InvalidTokenError:
        return Response({"error": "Invalid token"}, status=401)