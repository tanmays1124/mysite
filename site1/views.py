# from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse
from bson.objectid import ObjectId
from pymongo import MongoClient
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
import requests
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import UserQuiz, User
from django.template.context_processors import csrf
from django.shortcuts import get_object_or_404
import json
import datetime
from django.template.defaultfilters import safe
# from djongo import BulkWrite


# from django.utils import simplejson

# Connect to MongoDB
client = MongoClient()
db = client['quizviz']




# Login 


# when user tries to login
@csrf_protect
def user_login(request):
    if request.method=='POST':
        password = request.POST['password']
        uname = request.POST['uname']

        user = User.objects.filter(username=uname).first()

        if user is not None:
            c = {}
            c.update(csrf(request))
            # login(request, user)
            name = user.first_name
            # print(name)
            # if user.is_staff == True:
            #     return render(request, 'adminpage.html')
            
            request.session['username'] = uname
            return render(request, 'home.html',{'name':name}) 
             

        else:
            return HttpResponse("<h1>wrong credentials!<h1>")
    else:
        return render(request,'login.html')
            



# user registration
@csrf_protect
def register(request):
    try:
        n=''
        if request.method == 'POST':
            # Extract user information from the request
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            password = request.POST['password']
            cpassword = request.POST['Cpassword']
            uname = request.POST['username']



            user_exists = User.objects.filter(username=uname).first() or User.objects.filter(email=email).exists()



        
            if user_exists:
                messages.error(request, 'That username or email already exists')
                return redirect('register')

            else:

                if len(password) < 8:
                     messages.error(request, 'Password length should be greater than 8')
                     return redirect('register')
                elif password!=cpassword:
                    messages.error(request,"Password doesn't match")
                    return redirect('register')
                else:
                    hashed_password = make_password(password)
                    user_add = User(
                    email=email,
                    username=uname,
                    password=hashed_password,
                    first_name = fname,
                    last_name = lname
                    )
                    user_add.save()
                    
                    user_quiz = UserQuiz(username=uname,quiz_easy=[],quiz_medium=[],quiz_hard=[])
                    user_quiz.save()
                    
                    return redirect('user_login')            
            
        else:
            return render(request,'register.html')
    except Exception as e:
        print(e)
        messages.error(request,f"{e}")
        return HttpResponse("Error")
    


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
    data = db.questions.find({"category":"Linux","difficulty":"easy"})
    questions = []
    options = []
    answers =[]
    for i in data:
        questions.append(i["question"])
        option = []
        option.append(i["options"][0])
        option.append(i["options"][1])
        option.append(i["options"][2])
        option.append(i["options"][3])
        options.append(option)
        corr = i["answer"]
        answers.append(i["options"][corr])
        
    print(questions)
    print(options)

    data = {
            "answers": answers,
            "options": options,
            "questions": questions,
            "difficulty_lvl": 'easy'
            }

    data = json.dumps(data)
        
    return render(request,'quiz.html',{'data':data})





def medium(request):
    data = db.questions.find({"category":"Linux","difficulty":"medium"})
    questions = []
    options = []
    answers =[]
    for i in data:
        questions.append(i["question"])
        option = []
        option.append(i["options"][0])
        option.append(i["options"][1])
        option.append(i["options"][2])
        option.append(i["options"][3])
        options.append(option)
        corr = i["answer"]
        answers.append(i["options"][corr])
        
    print(questions)
    print(options)

    
    
    data = {
            "answers": answers,
            "options": options,
            "questions": questions,
            "difficulty_lvl": 'medium'
            }
    # return JsonResponse(data)
    data = json.dumps(data)
        
    return render(request,'quiz.html',{'data':data})






def difficult(request):
    data = db.questions.find({"category":"Linux","difficulty":"difficult"})
    questions = []
    options = []
    answers =[]
    for i in data:
        questions.append(i["question"])
        option = []
        option.append(i["options"][0])
        option.append(i["options"][1])
        option.append(i["options"][2])
        option.append(i["options"][3])
        options.append(option)
        corr = i["answer"]
        answers.append(i["options"][corr])
        
    print(questions)
    print(options)

    
    
    data = {
            "answers": answers,
            "options": options,
            "questions": questions,
            "difficulty_lvl": 'difficult'
            }
    # return JsonResponse(data)
    data = json.dumps(data)
        
    return render(request,'quiz.html',{'data':data})


def logout_view(request):
    logout(request)
    return redirect(user_login)

def feed(request):
    if request.method == 'POST':
        q_text = request.POST['question']
        o1 = request.POST['option1']
        o2 = request.POST['option2']
        o3 = request.POST['option3']
        o4 = request.POST['option4']
        corr = request.POST['correct']
        category = request.POST['category']
        difficulty = request.POST['difficulty']
        ind = 0
        if o1 == corr:
            ind=0
        elif o2 == corr:
            ind=1
        elif o3 == corr:
            ind=2
        elif o4 == corr:
            ind=3
        
        
        
        data = {
            "category":category,
            "difficulty": difficulty,
            "question": q_text,
            "options": [o1,o2,o3,o4],
            "answer": ind
        }

        db.questions.insert_one(data)
        return render(request,'adminpage.html')
    return render(request, 'adminpage.html')


def delete_user(request):
    username = request.session.get('username')
    user = get_object_or_404(User, username=username)
    user.delete()
    return redirect('user_login')



def updated_score(request):
    if request.method == 'POST':
        updated_score = request.POST.get('updated_data')
        difficulty_lvl = request.POST.get('difficulty')
        field =""

        if difficulty_lvl =='medium':
            field = "quiz_medium"
        elif difficulty_lvl =='easy':
            field = "quiz_easy"
        else:
            field = "quiz_hard"

        username=request.session.get('username')
        data = {
            "score":updated_score,
            "time": datetime.datetime.now(),

        }
        db.site1_userquiz.update_one({"username":username},{"$push":{field:data}})
        
    return HttpResponse('updated')


def history(request):
    uname = request.session.get("username")
    user = UserQuiz.objects.filter(username=uname).first()
    easy = user.quiz_easy if user.quiz_easy else None
    medium = user.quiz_medium if user.quiz_medium else None
    hard = user.quiz_hard if user.quiz_hard else None
    history =[]
    if easy:
        for i in easy:
            i['level'] = 'easy'
            history.append(i)
    if medium:
        for i in medium:
            i['level'] = 'medium'
            history.append(i)
    if hard:
        for i in hard:
            i['level'] = 'hard'
            history.append(i)

    history = sorted(history, key=lambda item: item['time'],reverse=True)
    print(history)
    

    
    return render(request,'history.html',{'history':history})

 