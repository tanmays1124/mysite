# from django.db import models
from django.db import models
# from django.contrib.postgres.fields import JSONField
# from djangotoolbox.fields import DictField,ListField
# from django.contrib.auth import get_user_model 
# from django.db.models.signals import post_save
# from djongo import database
# from django.dispatch import receiver

# Create your models here.

class Users(models.Model):
    name = models.CharField( max_length=50,null=False,blank=False)
    password = models.CharField( max_length=50,null=False,blank=False)
    email = models.CharField(max_length=50,null=False,blank=False)
    l = models.CharField(max_length=50,null=False,blank=False)
    
    def __str__(self):
        return f'{self.name} , {self.password}'
    
class Easy(models.Model):
    # ques = ListField()
    # ans = ListField()
    # time = ListField()
    # score = ListField()
    rank = models.IntegerField()

    


# @receiver(post_save, sender=Users)
# def create_user_collection(sender, instance, created, **kwargs):
#     if created:  
#         db = database.MongoClient().website 
#         collection = db.create_collection(instance.email)




# @receiver(post_save, sender=Users) 
# def create_user_collection(sender, instance, created, **kwargs):
#     if created:
#         db = mongoengine.connect(db='tanmay', host='localhost', port=27017)
#         mongo_client = db.client
#         mongo_db = mongo_client['tanmay']

# # Create collection
#         collection = mongo_db.create_collection('test_coll') 
#         print(collection)
# papa meri jaan 


