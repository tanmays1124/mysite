from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request,'index.html',{'name':'Tanmay'})

def submit(request):
    name = request.POST['name']
    return render(request,'success.html',{'name':name})

