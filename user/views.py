from django.shortcuts import render
from user.form import LoginForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


# def index(request):
#
#     return render(request, 'index.html')

def login(request):

    return render(request, 'login.html', {'form': LoginForm})

def sign_in(request):
    errors = []
    if request.method == 'POST':
        # print(request.POST.keys())
        if not request.POST.get('email', ''):
            errors.append('Введите email')
        if not request.POST.get('password', ''):
            errors.append('Введите пароль')
        if errors:
            print(errors)
            return render(request, 'login.html', {
                'form': LoginForm,
                'errors': errors,
                })
        return HttpResponseRedirect('/')

def registration(request):

    return render(request, 'registration.html')

