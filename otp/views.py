from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import Otp
from utils.otp import generate_otp
from .task import send_otp_email_task
from .serializers import SendOtpSerializer, VerifyOtpSerializer
from profiles.models import Profiles,UserLoggedIn,Coins

class SendOtpView(APIView):
    def post(self, request):
        serializer = SendOtpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = generate_otp()

            # Create or update OTP in DB
            otp_entry, _ = Otp.objects.update_or_create(
                email=email,
                defaults={"otp": otp_code, "exp": timezone.now() + timedelta(minutes=20)}
            )

            # Send OTP asynchronously
            send_otp_email_task.delay(email, otp_code)

            return Response({"message": f"OTP sent to {email}"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtpView(APIView):
    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp']

            # 🔹 Step 1: Get OTP
            try:
                otp_entry = Otp.objects.get(email=email)
            except Otp.DoesNotExist:
                return Response({"error": "OTP not found"}, status=status.HTTP_404_NOT_FOUND)

            # 🔹 Step 2: Check expiry
            if otp_entry.is_expired():
                return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)

            # 🔹 Step 3: Check match
            if otp_entry.otp != otp_code:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

            # 🔹 Step 4: OTP is valid → delete it
            otp_entry.delete()

            # 🔹 Step 5: Get or create user profile
            profile, created = Profiles.objects.get_or_create(
                Email=email,
                defaults={
                    "Username": email.split("@")[0],  # fallback username
                    "phone_number": "",
                    "gender": "O",  # default "Other"
                    "dob": "2000-01-01",  # default date
                    "name": email.split("@")[0],  # fallback name
                }
            )

            # 🔹 Step 6: Mark user as logged in
            UserLoggedIn.objects.update_or_create(
                user=profile,
                defaults={"is_logged_in": True}
            )
            if not Coins.objects.filter(user=profile):
                Coins.objects.create(user=profile)

            return Response({
                "message": "OTP verified successfully, user logged in!",
                "user_created": created
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(["POST"])
def LogoutUser(request):
    data = request.data
    email = data.get("email")
    try:
        user = Profiles.objects.get(Email = email)
        logged = UserLoggedIn.objects.get(user = user)
        logged.is_logged_in = False
    except Profiles.DoesNotExist or UserLoggedIn.DoesNotExist  :
         return Response({"message":"User Not Found"}, status=status.HTTP_400_BAD_REQUEST)

    
    



