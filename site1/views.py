from django.shortcuts import render
from django.http import HttpResponse
from .models import Users
# Create your views here.
def login(request):
    return render(request,'login.html')

def success(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['Cpassword']

        new_user = Users(name = name, password = password, email = email)
        new_user.save()
    
    return render(request,'success.html')

def register(request):
    return render(request,'register.html')

