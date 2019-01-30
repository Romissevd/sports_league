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
        help_text='Имя должно состоять из букв'
    )

    last_name = forms.CharField(
        max_length=50,
    )

    class Meta:

        model = User
        fields = ('first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2',
                  )
