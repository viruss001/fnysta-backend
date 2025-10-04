from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Profiles,BirthDetails,Coins
from .serializers import ProfileSerializer

@api_view(["GET"])
def getUser(request):
    email = request.query_params.get("email")  # get from query param ?email=...
    if not email:
        return Response({"message": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        profile = Profiles.objects.get(Email=email)
        serializer = ProfileSerializer(profile)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)
    except Profiles.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(["POST"])
def UserUpdator(request):
    data = request.data
    email = data.get("email")
    if not email:
        return Response({"message": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Check if profile exists
        profile = Profiles.objects.get(Email=email)
        # Update existing profile with incoming data
        serializer = ProfileSerializer(profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"user": serializer.data, "message": "User updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Profiles.DoesNotExist:
        
        return Response({"message": "User Not found"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
def GetDOB(request):
    email = request.query_params.get("email")

    if not email:
        return Response({"message": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        profile = Profiles.objects.get(Email=email)
        userdob = BirthDetails.objects.get(user=profile)
        return Response({
            "data": {
                "email": profile.Email,
                "time_of_birth": str(userdob.time_of_birth),
                "place_of_birth": userdob.place_of_birth
            }
        })
    except Profiles.DoesNotExist:
        return Response({"message": "User Not found"}, status=status.HTTP_404_NOT_FOUND)
    except BirthDetails.DoesNotExist:
        return Response({"message": "Birth details not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def UpdateDOB(request):
    email = request.query_params.get("email")

    if not email:
        return Response({"message": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data
    time_of_birth = data.get("tob")
    place_of_birth = data.get("top")

    try:
        profile = Profiles.objects.get(Email=email)
        userdob, created = BirthDetails.objects.update_or_create(
            user=profile,
            defaults={
                "time_of_birth": time_of_birth,
                "place_of_birth": place_of_birth
            }
        )
        return Response({
            "data": {
                "email": profile.Email,
                "time_of_birth": str(userdob.time_of_birth),
                "place_of_birth": userdob.place_of_birth,
                "created": created
            }
        })
    except Profiles.DoesNotExist:
        return Response({"message": "User Not found"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["GET"])
def getCoin(request):
    email = request.query_params.get("email")
    try:
        profile = Profiles.objects.get(Email=email)
        coins = Coins.objects.get(user = profile)
        return Response({"coins":coins.coins})
    except Profiles.DoesNotExist:
        return Response({"message": "User Not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def Updatecoin(request):
    email = request.query_params.get("email")

    try:
        profile = Profiles.objects.get(Email=email)
        coins = Coins.objects.get(user = profile)
        coins.coins = coins.coins+10
        coins.save()
        return Response({"coins":coins.coins})
    except Profiles.DoesNotExist:
        return Response({"message": "User Not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def UpdatecoinBYValue(request):
    email = request.query_params.get("email")
    if not email:
        return Response({"message": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        coin_value = int(request.data.get("coin", 0))
    except (TypeError, ValueError):
        return Response({"message": "Invalid coin value"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        profile = Profiles.objects.get(Email=email)
        coins, _ = Coins.objects.get_or_create(user=profile)
        coins.coins += coin_value
        coins.save()
        return Response({"coins": coins.coins})
    except Profiles.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)







'''

Email address: admin@admin.com
Password: admin


{
  "email": "iamsurajtiwari1909@gmail.com",
  "Username": "surajtiwari",
  "phone_number": "+919876543210",
  "gender": "M",
  "dob": "1995-09-26",
  "name": "Suraj Tiwari"
}
        
'''