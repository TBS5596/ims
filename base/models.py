from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    date_of_birth = models.DateField(auto_now=True)
    phone_no = models.CharField(max_length=12)
    address = models.CharField(max_length=255)
    position = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}' profile"
