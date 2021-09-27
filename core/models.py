from django.db import models

# Create your models here.
class Optionchain(models.Model):
    Symbol = models.CharField(max_length=50)
    Expiry = models.DateField(auto_now=False)
    Date = models.DateField(auto_now=False)
    SpotPrice = models.CharField(max_length=50)
    CallDelta = models.CharField(max_length=50)
    CallIV = models.CharField(max_length=50)
    CallLTP = models.CharField(max_length=50)
    CallVega = models.CharField(max_length=50)
    Strikes = models.CharField(max_length=50)
    PutDelta = models.CharField(max_length=50)
    PutLTP = models.CharField(max_length=50,default='none')
    PutIV = models.CharField(max_length=50)
    Lotsize = models.CharField(max_length=50)




class SpotPrice(models.Model):
    Symbol = models.CharField(max_length=50)
    Date = models.DateField(auto_now=False)
    SpotPrice = models.CharField(max_length=50)