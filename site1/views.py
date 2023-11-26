from django.shortcuts import render
from django.http import HttpResponse
from .models import Users
# Create your views here.
def login(request):
    return render(request,'login.html')

def success(request):
    if request.method=='POST':
        usr = request.POST['username']
        passwd = request.POST['password']

        new_user = Users(usr=usr, password=passwd)
        new_user.save()

    return render(request,'success.html',{'username':usr,'pass':passwd})

