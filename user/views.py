from django.shortcuts import render
from user.form import LoginForm
from django.http import HttpResponse, HttpResponseRedirect
from user.models import User


class UserSignIn:

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


def login(request):

    return render(request, 'login.html', {'form': LoginForm})


def logout(request):

    return render(request, 'index.html', {'user': False})


def sign_in(request):
    # проверить если пользователь уже авторизован то перенаправить его на главную
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
        user_sign_in = User.objects.get(
            email=request.POST['email'],
            password=request.POST['password']
        )
        if not user_sign_in:
            errors.append('Неверно введен email или пароль.')
            return render(request, 'login.html', {
                'form': LoginForm,
                'errors': errors,
            })
        else:
            user = UserSignIn(
                user_sign_in.first_name,
                user_sign_in.last_name,
                )
            return render(request, 'index.html', {
                'user': user,
            })
        # return HttpResponseRedirect('/')


def registration(request):

    return render(request, 'registration.html')
