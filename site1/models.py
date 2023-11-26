from django.db import models

# Create your models here.

class Users(models.Model):
    usr = models.CharField( max_length=50,null=False,blank=False)
    password = models.CharField( max_length=50,null=False,blank=False)