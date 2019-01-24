from django.shortcuts import render
from user.form import LoginForm
from django.http import HttpResponse


# def index(request):
#
#     return render(request, 'index.html')

def login(request):

    return render(request, 'login.html', {'form': LoginForm})

def registration(request):

    return render(request, 'registration.html')

