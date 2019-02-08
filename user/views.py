from django.shortcuts import render
from .form import LoginForm, RegistrationForm, ChangeUserForm
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile


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

    else:
        return render(request, 'login.html', {'form': LoginForm})


def sign_up(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

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
        return render(request, 'registration.html', {
            'form': RegistrationForm,
        })


def account(request, name=None):

    if request.method == 'POST':
        if change_account_save(request):
            return change_account(request, 'Имя и фамилия дожны состоять только из букв.')

    if name:
        # проверить есть ли пользователь?
        try: pass

        except: pass
        return render(request, 'account.html', {
            'view_user': User.objects.get(username=name),
        })

    return render(request, 'account.html', {
        'view_user': User.objects.get(username=request.user),
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
        gender = form.cleaned_data.get('gender')
        country = form.cleaned_data.get('country')
        city = form.cleaned_data.get('city')
        about_me = form.cleaned_data.get('about_me')
        date_of_birth = form.cleaned_data.get('date_of_birth')

        if first_name:
            if first_name.isalpha():
                user.first_name = first_name
            else:
                return True

        if last_name:
            if last_name.isalpha():
                user.last_name = last_name
            else:
                return True

        if gender:
            user.profile.gender = gender

        if country:
            user.profile.country = country

        if city:
            user.profile.city = city

        if date_of_birth:
            user.profile.date_of_birth = date_of_birth

        if about_me:
            user.profile.about_me = about_me

        user.save()
        user.profile.save()

    return None


def all_users(request):

    users = User.objects.all()

    return render(request, 'users.html', {
        'all_users': users,
    })
