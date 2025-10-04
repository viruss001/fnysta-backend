from django.db import models


class Profiles(models.Model):
    GENDER_CHOICES = [
        
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    Email = models.EmailField(primary_key=True) 
    Username = models.CharField(max_length=100,null=True, blank=True)
    phone_number = models.CharField(max_length=13,null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', null=True, blank=True)  # optional
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=100,null=True, blank=True)



    def __str__(self):
        return self.Email
class BirthDetails(models.Model):
    user = models.OneToOneField(Profiles, on_delete=models.CASCADE)
    time_of_birth = models.TimeField() 
    place_of_birth = models.TextField()


class Coins(models.Model):
    user = models.OneToOneField(Profiles, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)

class UserLoggedIn(models.Model):
    user = models.OneToOneField(Profiles, on_delete=models.CASCADE, related_name="login_status")
    is_logged_in = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)  # optional: track login time

    def __str__(self):
        return f"{self.user.Email} - {'Logged in' if self.is_logged_in else 'Logged out'}"

