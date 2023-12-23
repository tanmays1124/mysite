from djongo import models

class Questions(models.Model):
  id = models.ObjectIdField(max_length=100,null=False,blank=True) 
  str = models.CharField(max_length = 500)
  class Meta:
    abstract = True




class User(models.Model):
    username = models.CharField(max_length=150, unique=True, default='default_username')
    first_name = models.CharField(max_length=30,default='fname')
    last_name = models.CharField(max_length=30,default='lname')
    email = models.EmailField(unique=True, default='default@example.com')
    password = models.CharField(max_length=128,default='fname')

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

