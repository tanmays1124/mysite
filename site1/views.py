from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Users
from django.db import models
from djongo import database
from django.db import connections
import pymongo

db = database.MongoClient().tanmay
# Create your views here.

# Login 
def login(request):
    return render(request,'login.html')



# when user tries to login
def result(request):
    all_instances = Users.objects.all()
    f=0
    if request.method=='POST':
        password = request.POST['password']
        email = request.POST['email']
        
         


        from django.db import connections

        connection = connections['default']
        db = connection.cursor().get_database("tanmay")
        collections = db.list_collection_names()

        print("Collections in my_database:")
        for collection in collections:
            print(collection)


        for i in all_instances:
            if i.email==email and i.password==password:
                col = db[email]
                doc = col.find_one() 
                data = {
                    'name': i.name,
                    'score1': doc['score_Linux'][0],
                    'score2': doc['score_Linux'][1],
                    'score3': doc['score_Linux'][2]
                }
                return render(request, 'home.html',data)
            else:
                f=1
    if f==1:
        # return render(request,'result.html',{'details' : all_instances})
        return HttpResponse('<h1> user does not exists</h1>')

# def update(request):
#     col = db['site1_users']

#     update = {"$set": { "name": 'Tanmay Sharan' }}
#     result = col.update_one({"name":"John Cena"}, update)

#     print(result.modified_count)
#     return HttpResponse('<h1>Good<h1>')


def res(request):
    return render(request, 'result.html')



# user registration
def register(request):
    return render(request,'register.html')

# when user successfully registered in
def registering(request):
    n=''
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['Cpassword']

        new_user = Users(name = name, password = password, email = email)
        new_user.save()
        n=name
    
    return home(request,n)





def home(request,name):
    return render(request, 'home.html',{'name':name})





