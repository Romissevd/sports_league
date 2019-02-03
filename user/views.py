from django.shortcuts import render
from .form import LoginForm, RegistrationForm, ChangeUserForm
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile


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
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            if not first_name.isalpha() or not last_name.isalpha():
                return render(request, 'registration.html', {
                    'form': form,
                    'error': 'Имя и фамилия дожны состоять только из букв.'
                })

            try:
                User.objects.get(username=email)
            except User.DoesNotExist:
                pass
            else:
                return render(request, 'registration.html', {
                    'form': form,
                    'error': 'Увы, пользователь с таким email уже зарегестирован.'
                })

            profile_user = User.objects.create_user(
                username=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )

            Profile.objects.create(user=profile_user)

            user = auth.authenticate(username=email, password=password)
            auth.login(request, user)

            return HttpResponseRedirect('{}'.format(request.path))

        else:
            print(form.errors)
            return render(request, 'registration.html', {
                'form': form,
            })

    else:
        return HttpResponseRedirect('{}'.format(request.path))


def account(request):

    if request.method == 'POST':
        if change_account_save(request):
            return change_account(request, 'Имя и фамилия дожны состоять только из букв.')

    return render(request, 'account.html', {
        'user': User.objects.get(username=request.user),
    })


def change_account(request, error=''):

    return render(request, 'change_account.html', {
        'form': ChangeUserForm,
        'error': error,
    })


def change_account_save(request):

    form = ChangeUserForm(request.POST)
    if form.is_valid():
        user = User.objects.get(username=request.user)

        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        if not first_name.isalpha() or not last_name.isalpha():
            return True
        else:
            user.first_name = first_name
            user.last_name = last_name

        user.profile.gender = form.cleaned_data.get('gender')
        user.profile.country = form.cleaned_data.get('country')
        user.profile.city = form.cleaned_data.get('city')
        user.profile.about_me = form.cleaned_data.get('about_me')
        user.save()
        user.profile.save()

    return None
