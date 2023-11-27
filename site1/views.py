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





def result(request):
    all_instances = Users.objects.all()
    f=0
    if request.method=='POST':
        password = request.POST['password']
        email = request.POST['email']
    for i in all_instances:
        if i.email==email and i.password==password:
            return render(request, 'home.html')
        else:
            f=1
    if f==1:
        # return render(request,'result.html',{'details' : all_instances})
        return HttpResponse('<h1> user does not exists</h1>')




def home(request):
    return render(request, 'home.html')




