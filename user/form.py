from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):

    email = forms.EmailField(
        label='Email:'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        max_length=30,
        label='Пароль:',
    )


class RegistrationForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=30,
        help_text='Имя должно состоять из букв',
    )

    last_name = forms.CharField(
        max_length=50,
    )

    email = forms.EmailField()

    class Meta:

        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            )


class ChangeUserForm(forms.Form):

    user_avatar = forms.ImageField(
        required=False,
    )

    first_name = forms.CharField(
        max_length=30,
        help_text='Имя должно состоять из букв',
        required=False,
    )

    last_name = forms.CharField(
        max_length=50,
        required=False,
    )

    gender = forms.ChoiceField(
        widget=forms.Select(),
        choices=([('', ''), ('Мужской', 'Мужской'), ('Женский', 'Женский'), ]),
        initial='',
        required=False,
    )

    date_of_birth = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
        required=False,
    )

    # можно использовать django-countries https://github.com/SmileyChris/django-countries
    country = forms.CharField(
        max_length=50,
        required=False,
    )

    city = forms.CharField(
        max_length=100,
        required=False,
    )

    about_me = forms.CharField(
        widget=forms.Textarea,
        required=False,
    )
