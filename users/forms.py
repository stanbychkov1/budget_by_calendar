from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       UsernameField)
from django.forms import CharField, PasswordInput, TextInput

from .models import User


class UserAuthForm(AuthenticationForm):
    username = UsernameField(label='Пользователь',
                             widget=TextInput(attrs={'autofocus': True}))
    password = CharField(
        label='Пароль',
        strip=False,
        widget=PasswordInput(attrs={'autocomplete': 'current-password'}),
    )


class UserRegistrationForm(UserCreationForm):
    password2 = None

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'username', 'email')
