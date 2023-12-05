from django.db import models

# Create your models here.

class Users(models.Model):
    name = models.CharField( max_length=50,null=False,blank=False)
    password = models.CharField( max_length=50,null=False,blank=False)
    email = models.CharField(max_length=50,null=False,blank=False)
    
    def __str__(self):
        return f'{self.name} , {self.password}'


# models.py
class Hotel(models.Model):
	name = models.CharField(max_length=50)
	hotel_Main_Img = models.ImageField(upload_to='images/')
