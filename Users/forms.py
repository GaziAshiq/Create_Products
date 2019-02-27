from django import forms
from django.contrib.auth.models import User


class CreateProduct(forms.Form):
    title = forms.CharField(required=True, label='Title', min_length=5,
                            widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Description:"}))
    description = forms.CharField(min_length=150)
    url = forms.URLField()
    icon = forms.ImageField()
    image = forms.ImageField()


class UserSignup(forms.Form):
    username = forms.CharField(label='User Name', min_length=4, max_length=12, required=True,
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'User Name:', 'class': 'form-control', 'id': 'inputUserName'}))
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'Email:', 'class': 'form-control', 'id': 'inputEmail'}))
    password = forms.CharField(label='Password', min_length=6, required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm password', min_length=6, required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))

    def clean_password2(self):
        us = self.cleaned_data
        pass1 = self.cleaned_data.get('password')
        pass2 = self.cleaned_data.get('password2')
        if pass2 != pass1:
            raise forms.ValidationError('Password Must Match!')
        return us

    def clean_username(self):
        un = self.cleaned_data.get('username')
        user_model = User.objects.filter(username=un)
        if user_model.exists():
            raise forms.ValidationError('User Name Already Taken!')
        else:
            return un

    def clean_email(self):
        em = self.cleaned_data.get('email')
        em_model = User.objects.filter(email=em)
        if em_model.exists():
            raise forms.ValidationError('This Email Already Used by different user')
        else:
            return em


class UserLogin(forms.Form):
    username = forms.CharField(required=True, label='User Name or Email')
