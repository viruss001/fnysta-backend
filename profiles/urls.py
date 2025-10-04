from django.urls import path
from .views import UserUpdator ,getUser,UpdateDOB,GetDOB,getCoin,Updatecoin,UpdatecoinBYValue

urlpatterns = [
    path('Update-user/',UserUpdator , name='updateUser'),
    path('get-user/',getUser , name='GetUser'),
    path('get-dob/',GetDOB , name='getdob'),
    # path('getdob/', , name='GetUser'),
    path('update-dob/',UpdateDOB , name='updatedob'),
    path("get-coin/",getCoin),
    path("Update-coin/",Updatecoin),
    path("Update-coin-by-value/",UpdatecoinBYValue)
]

