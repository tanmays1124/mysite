# from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse
from bson.objectid import ObjectId
from pymongo import MongoClient
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
import requests
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import UserQuiz 
from django.template.context_processors import csrf
from django.shortcuts import get_object_or_404
import json
from django.template.defaultfilters import safe

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
            c = {}
            c.update(csrf(request))
            # login(request, user)
            name = user.first_name
            # print(name)
            if user.is_staff == True:
                return render(request, 'adminpage.html')
            else:
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
                    User.objects.create_user(
                    email=email,
                    username=uname,
                    password=hashed_password,
                    first_name = fname,
                    last_name = lname
                    )
                    
                    UserQuiz.object.create_user(username=uname,quiz_easy=[],quiz_medium=[],quiz_hard=[])
                    
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
            "questions": questions
            }
    # data = {
    #     'questions': ['Question 1', 'Question 2', 'Question 3'],
    #     'options': [['Option A', 'Option B', 'Option C', 'Option D']] * 3,
    #     'answers': ['Option A', 'Option B', 'Option C'],
    # }
    # encoded_data = json.dumps(data)
    # return render(request, 'quiz.html', {'encoded_data': safe(encoded_data)})

    
        
    return render(request,'quiz.html',data)





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
            "questions": questions
            }

    
        
    return render(request,'quiz.html',data)






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
            "questions": questions
            }

    
        
    return render(request,'quiz.html',data)


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

