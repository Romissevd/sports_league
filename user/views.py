from django.shortcuts import render
from .form import LoginForm, RegistrationForm
from django.http import HttpResponseRedirect
from django.contrib import auth


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
        # print(form)
        if form.is_valid():
            print("OK")
            # form.cleaned_data.update(username=form.cleaned_data['email'])
            form.save()
            email = form.cleaned_data.get('email')
            print(email)
            my_password = form.cleaned_data.get('password1')
            user = auth.authenticate(username=email, password=my_password)
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'registration.html', {
                'form': RegistrationForm,
            })

    else:
        return HttpResponseRedirect('/')
