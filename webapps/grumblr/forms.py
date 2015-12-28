from models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password did not match.")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        return username


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = {"password1", "password2", "first_name", "last_name",  "age", "short_bio", "image"}
        widgets = {'password1': forms.PasswordInput(), 'password2': forms.PasswordInput(), 'image': forms.FileInput()}

    def clean(self):
        cleaned_data = super(ProfileEditForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password did not match.")

        return cleaned_data

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1 == "":
            raise forms.ValidationError("Password is emtpy.")

        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')

        if password2 == "":
            raise forms.ValidationError("Comfirm password is emtpy.")

        return password2






