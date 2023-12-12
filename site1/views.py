from django.shortcuts import render,redirect
from django.http import HttpResponse
from bson.objectid import ObjectId
from pymongo import MongoClient
# from django.utils import simplejson

# Connect to MongoDB
client = MongoClient()
db = client['quiz']




# Login 
def login(request):
    return render(request,'login.html')


# when user tries to login
def result(request):
    f=0
    if request.method=='POST':
        password = request.POST['password']
        uname = request.POST['uname']


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



def registering(request):
    n=''
    if request.method == 'POST':
        # Extract user information from the request
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        uname = request.POST['username']



        username = db.user.find({'username':uname}).count()
        print(username)
        if username == 0:
            
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
                "questions": {
                    'easy':
                    {
                        'linux':
                        {
                            'q_txt': [],
                            'answered_correctly': [],
                            'time': ['2:30','3:00','5:20'],
                            'score':[23,45,12]
                        }
                    }
                },
            }
            db.quizzes.insert_one(quiz_data)
            return home(request,n)            
        else:
            return HttpResponse("User exists")

def home(request,name):
    return render(request, 'home.html',{'name':name})
import json
def dashboard(request):
    user_id = db.users.find_one({'username':'tanmays1124'},{'_id':1})
    print(str(user_id['_id']))

    score = db.quizzes.aggregate([{
        '$match':{'user_id': ObjectId(user_id['_id'])}
        },{
            '$project' :{'questions.easy.linux.score':1,'_id': 0}
        }
    ])
    list=0
    for sc in score:
        list=sc['questions']['easy']['linux']['score']


    return render(request,'dashboard.html',{'data':list})