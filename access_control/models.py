from django.db import models
from user_auth import models

class Tag(models.Model):
    member = models.ForeignKey('user_auth.Member', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=20)
