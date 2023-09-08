from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from clients.models import Author


class AuthorRegisterForm(UserCreationForm):
    class Meta:
        model = Author
        fields = ('email', 'password1', 'password2')


class AuthorProfileForm(UserChangeForm):
    class Meta:
        model = Author
        fields = ('email', 'full_name', 'organization', 'avatar',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
