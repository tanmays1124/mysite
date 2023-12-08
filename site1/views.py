from django.shortcuts import render,redirect
from django.http import HttpResponse
# from .models import Users
# from django.db import models
# from djongo import database
# from django.db import connections
import pymongo
from bson.objectid import ObjectId
# db = database.MongoClient().tanmay
# Create your views here.

# Login 
def login(request):
    return render(request,'login.html')


# when user tries to login
def result(request):
    f=0
    if request.method=='POST':
        password = request.POST['password']
        uname = request.POST['uname']
        
        
        
        client = MongoClient()

        db = client['quiz']
        


        user_data = db.users.find_one({'username':uname})
        print(user_data)

        if user_data:

            if user_data['password'] == password:
                data = {
                    'name': user_data['name'],
                    'score1': user_data['ranks']['easy']['linux'],
                    'score2': user_data['ranks']['medium']['linux'],
                    'score3': user_data['ranks']['difficult']['linux'],
                }
                return render(request, 'home.html',data)               

            else:
                return render(request,"wrong password")
            
        return HttpResponse('<h1> user does not exists</h1>')



def res(request):
    return render(request, 'result.html')



# user registration
def register(request):
    return render(request,'register.html')





from pymongo import MongoClient

def registering(request):
    n=''
    if request.method == 'POST':
        # Extract user information from the request
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        uname = request.POST['username']

        # Connect to MongoDB
        client = MongoClient()
        db = client['quiz']

        username = db.users.find({'username':uname})

        if username is None:
            
            n=name
            # Build user document
            user_data = {
                "_id": ObjectId(),
                "name": name,
                "username": uname,
                "email": email,
                "password": password,
                "quiz_id": ObjectId(),
                "scores": {
                    "easy":
                    {
                        "linux": 0,
                        "sql": 0,
                        "nosql": 0
                    },
                    "medium":
                    {
                        "linux": 0,
                        "sql": 0,
                        "nosql": 0
                    },
                    "difficult":
                    {
                        "linux": 0,
                        "sql": 0,
                        "nosql": 0
                    }
                },
                "ranks": {
                    "easy":
                    {
                        "linux": "Not Ranked",
                        "sql": "Not Ranked",
                        "nosql": "Not Ranked"
                    },
                    "medium":
                    {
                        "linux": "Not Ranked",
                        "sql": "Not Ranked",
                        "nosql": "Not Ranked"
                    },
                    "difficult":
                    {
                        "linux": "Not Ranked",
                        "sql": "Not Ranked",
                        "nosql": "Not Ranked"
                    }
                }
            }

            # Insert user document
            db.users.insert_one(user_data)

            # Create empty quiz document
            quiz_data = {
                "_id": ObjectId(),
                "user_id": user_data['_id'],
                "questions": [],
            }
            db.quizzes.insert_one(quiz_data)
            return home(request,n)            
        else:
            return HttpResponse("User exists")
    
    




















# # when user successfully registered in
# def registering(request):
#     n=''
#     if request.method=='POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         password = request.POST['password']
#         cpassword = request.POST['Cpassword']

#         ranks = "Not Ranked"

#         data = {
#             "_id": ObjectId(),
#             "name": name,
#             "email": email,
#             "password": password,
#             "questions":{
#                 "easy": {
#                     "linux":{
#                         "q_text": [],
#                         "correct": [],
#                         "time": [],
#                         "score": [],
#                         "rank": ranks
#                     }
#                 },
#                 "medium": {
#                     "linux":{
#                         "q_text": [],
#                         "correct": [],
#                         "time": [],
#                         "score": [],
#                         "rank": ranks
#                     }
#                 },
#                 "hard": {
#                     "linux":{
#                         "q_text": [],
#                         "correct": [],
#                         "time": [],
#                         "score": [],
#                         "rank": ranks
#                     }
#                 }
#             }
#         }

#         db = pymongo.MongoClient()["quiz"]
#         db.site1_users.insert_one(data)

#         # new_user = Users(name = name, password = password, email = email)
#         # new_user.save()

#         n=name
    
#     return home(request,n)





def home(request,name):
    return render(request, 'home.html',{'name':name})