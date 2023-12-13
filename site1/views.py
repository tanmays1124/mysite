from django.shortcuts import render,redirect
from django.http import HttpResponse
from bson.objectid import ObjectId
from pymongo import MongoClient
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
import requests

# from django.utils import simplejson

# Connect to MongoDB
client = MongoClient()
db = client['quiz']




# Login 


# when user tries to login
@csrf_protect
def user_login(request):
    if request.method=='POST':
        password = request.POST['password']
        uname = request.POST['uname']

        user = authenticate(username=uname, password=password)

        if user is not None:
            login(request, user)
            name = user.first_name
            

            user_data = db.users.find_one({'username':uname})

            data = {
                        'name': name,
                        'score1': user_data['ranks']['easy']['linux'],
                        'score2': user_data['ranks']['medium']['linux'],
                        'score3': user_data['ranks']['difficult']['linux'],
                    }
            return render(request, 'home.html',data) 
             

        else:
            return HttpResponse("<h1>wrong credentials!<h1>")
    else:
        return render(request,'login.html')
            



# user registration
@csrf_protect
def register(request):
    n=''
    if request.method == 'POST':
        # Extract user information from the request
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        uname = request.POST['username']

        # myuser = User.objects.create_user(username = uname, email = email, password = password,fname = fname,lname = lname)
        # myuser.save()



        username = db.users.find({'username':uname}).count()
        print(username)
        if username == 0:
            myuser = User.objects.create_user(username = uname, email = email, password = password,first_name = fname,last_name = lname)
            myuser.save()
            
            fn=fname
            ln=lname
            # Build user document
            user_data = {
                "_id": ObjectId(),
                "fname": fn,
                "lname": ln,
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
            return redirect('user_login')            
        else:
            return HttpResponse("User exists")
    else:
        return render(request,'register.html')
    


def home(request,fname,lname):
    return render(request, 'home.html',{'fname':fname,'lname':lname})


def dashboard(request):
    user_id = db.users.find_one({'username':'tanmays1124'},{'_id':1})
    print(str(user_id['_id']))

    data = db.quizzes.aggregate([{
        '$match':{'user_id': ObjectId(user_id['_id'])}
        },{
            '$project' :{'questions.easy.linux.score':1,'questions.easy.linux.time':1,'_id': 0}
        }
    ])
    list1=0
    list2=0
    for sc in data:
        list1=sc['questions']['easy']['linux']['score']
        list2=sc['questions']['easy']['linux']['time']
    print(list(list2))
    

    return render(request,'dashboard.html',{'scores':list1,'time':list2})






# def appview(request):
#     # Set the parameters for the API 
#     api_url = 'https://quizapi.io/api/v1/questions'
#     apiKey = 'EvJrmL7hr1UcZBglIp9zd6nXhLb1rXl2fRUnrfvg'
#     params={
#         'apiKey':apiKey,
#         'category' : 'linux',
#         'difficulty':'Medium',
#         'limit':10
#         }

#         # Make the API request
#     response = requests.get('https://quizapi.io/api/v1/questions?apiKey=EvJrmL7hr1UcZBglIp9zd6nXhLb1rXl2fRUnrfvg').json()
    

#     data = response
#     print(data)
#     return HttpResponse('got it')



def easy(request):
    data = db.questions.find({"difficulty":"easy"})
    questions = []
    options = []
    answers =[]
    for i in data:
        questions.append(i["question"])
        option = []
        option.append(i["options"][0]["a"])
        option.append(i["options"][1]["b"])
        option.append(i["options"][2]["c"])
        option.append(i["options"][3]["d"])
        options.append(option)
        corr = i["answer"]
        index = 0
        if corr == "a":
            index = 0
        elif corr == "b":
            index = 1
        elif corr == "c":
            index = 2
        else:
            index = 3
        answers.append(i["options"][index][corr])
    print(questions)
    print(options)

    data = {
            "answers": answers[0],
            "options": options[0],
            "questions": questions[0]
            }

    
        
    return render(request,'quiz.html', data)