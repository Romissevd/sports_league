from django import forms

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