from djongo import models

class Questions(models.Model):
    id = models.ObjectIdField(primary_key=True) 
    str = models.CharField(max_length = 500)



class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True, default='default_username')
    password = models.CharField(max_length=100)
    reset_password_token = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.username
    
class QuizAttempt(models.Model):
   score = models.IntegerField()
   time = models.DateTimeField()
   questions = models.ArrayField(model_container=Questions)
   answers = models.ArrayField(model_container=Questions)
   
   class Meta:
     abstract = True




class UserQuiz(models.Model):
    username = models.CharField(max_length = 100,null=True,blank=True)

    quiz_easy = models.ArrayField(
      model_container=QuizAttempt
   )
    quiz_medium = models.ArrayField(
      model_container=QuizAttempt
   ) 
    quiz_hard = models.ArrayField(
      model_container=QuizAttempt
   )

