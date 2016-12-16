from django import forms
from django.contrib.auth.models import User
from wallet.models import Userprofile
from django.core.validators import RegexValidator


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ('date_ob', 'sex')


class UserReg(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, validators=[RegexValidator(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,20}', message="Password should contain Minimum 8 characters, at least 1 Uppercase Alphabet, 1 Lowercase Alphabet, 1 Number and 1 Special Character")])
    username = forms.CharField(min_length=5)

    class Meta:
        model = User
        fields = ['username', 'password']

