from django.db import models
from django.conf import settings

class Tag(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=20, primary_key=True)
