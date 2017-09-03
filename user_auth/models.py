from django.db import models
from django.conf import settings

# User Profile
class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    address = models.CharField(max_length=35)
    address1 = models.CharField(max_length=35)
    city = models.CharField(max_length=35)
    postcode = models.CharField(max_length=35)
    phone = models.CharField(max_length=40)
    membership_expiry = models.DateField(auto_now_add=True)
    emergency_information = models.CharField(max_length=1024)

class MemberEmergencyContacts(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    phone = models.CharField(max_length=40)

# Social media usernames
class MemberSocialMedia(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    site = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
