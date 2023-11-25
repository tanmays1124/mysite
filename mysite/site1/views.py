from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def login(request):
    return render(request,'login.html')

def success(request):
    usr = request.POST['username']
    passwd = request.POST['password']
    return render(request,'success.html',{'username':usr,'pass':passwd})

