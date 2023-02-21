from django.shortcuts import render
from django.http import HttpResponse

# How to get all users info
# from django.contrib.auth.models import User
# all_users = User.objects.all().values()

# Create your views here.
def index(request):
    
    user = request.user
    data ={
        'user' : user
    }
    
    return render(request, "main/main_page.html", data)

def about(request):
    return render(request, "main/info.html")