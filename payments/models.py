from django.db import models
from user_auth import models

class Payments(models.Model):
    PAYMENT_TYPES = (
        ('gocardless', 'Go Cardless'),
        ('barclays', 'Barclays Bank Transfer'),
        ('coop', 'Co-Op Bank Transfer'),
        ('cash', 'Cash to board member'),
    )

    member = models.ForeignKey('user_auth.Member', on_delete=models.CASCADE)
    source = models.CharField(choices=PAYMENT_TYPES, default='gocardless', max_length=2)
    amount = models.Decimalfield(max_digits=8, decimal_places=2)
    reference = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)
