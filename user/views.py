from django.shortcuts import render
from .form import LoginForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from .models import User


class UserSignIn:

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


def login(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    return render(request, 'login.html', {'form': LoginForm})


def logout(request):

    auth.logout(request)
    return HttpResponseRedirect('/')


def sign_in(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    errors = []
    if request.method == 'POST':
        if not request.POST.get('email', ''):
            errors.append('Введите email')
        if not request.POST.get('password', ''):
            errors.append('Введите пароль')
        if errors:
            return render(request, 'login.html', {
                'form': LoginForm,
                'errors': errors,
                })

        user = auth.authenticate(
            username=request.POST['email'],
            password=request.POST['password'],
        )

        if user is not None:
            auth.login(request, user)
        return HttpResponseRedirect('/')




def registration(request):

    return render(request, 'registration.html')
