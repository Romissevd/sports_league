from django.shortcuts import render
from .form import LoginForm, RegistrationForm
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User


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
        email = request.POST.get('email', '')
        passwd = request.POST.get('password', '')
        if not email:
            errors.append('Введите email')
        if not passwd:
            errors.append('Введите пароль')
        if errors:
            return render(request, 'login.html', {
                'form': LoginForm,
                'errors': errors,
                })

        user = auth.authenticate(
            username=email,
            password=passwd,
        )

        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            errors.append('Неверные email или пароль.')
            errors.append('Попробуйте еще раз.')
            return render(request, 'login.html', {
                'form': LoginForm,
                'errors': errors,
            })


def registration(request):

    return render(request, 'registration.html', {
        'form': RegistrationForm,
    })


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            try:
                User.objects.get(username=email)
            except User.DoesNotExist:
                pass
            else:
                return render(request, 'registration.html', {
                    'form': form,
                    'error': 'Увы, пользователь с таким email уже зарегестирован.'
                })

            User.objects.create_user(
                username=email,
                password=password,
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                email=email,
            )
            user = auth.authenticate(username=email, password=password)
            auth.login(request, user)
            return HttpResponseRedirect('/')

        else:
            print(form.errors)
            return render(request, 'registration.html', {
                'form': form,
            })

    else:
        return HttpResponseRedirect('/')
