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

            User.objects.create_user(
                username=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )

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

    if request.method=='POST':
        change_account_save(request)


    user_data = User.objects.get(username=request.user)

    return render(request, 'account.html', {
        'user_data': user_data,
    })


def change_account(request):

    # form = ChangeUser

    return render(request, 'change_account.html', {
        'form': ChangeUserForm,
    })


def change_account_save(request):
    form = ChangeUserForm(request.POST)
    if form.is_valid():
        user = User.objects.get(username=request.user)
        # User.objects.update(
        #     email=form.cleaned_data.get('email'),
        #     # profile__gender=form.cleaned_data.get('gender'),
        #     # profile__country=form.cleaned_data.get('country'),
        #     # profile__city=form.cleaned_data.get('city'),
        # )
        # Profile(user=user,
        # # user.profile.objects.update(
        #     gender=form.cleaned_data.get('gender'),
        #     country=form.cleaned_data.get('country'),
        #     city=form.cleaned_data.get('city'),
        # )
    return None
