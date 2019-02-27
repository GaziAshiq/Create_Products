from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import UserSignup


# TODO problem: when user login, they can access login and signup page without Logout


# Create your views here.

# def signup(request):
#     """
#     this is my old method for creating new user, but there is a problem about password algorithm, that's why now
#     i create signup_v1, enjoy
#     :param request:
#     :return:
#     """
#     # TO-DO(Fixed by signup_v1) : there is a bug. user can sign up successfully, but django not using hashing for
#     # password. so when
#     #  new user try to login, it throw an error, because password hashing algorithm not working. i have to look at it
#
#     if request.method == 'POST':
#         if request.POST['pass1'] == request.POST['pass2']:  # if both password match
#             print(request.POST['pass1'])
#             try:
#                 user = User.objects.get(username=request.POST['username'])
#                 user.set_unusable_password()
#                 user.save()
#                 return render(request, 'users/signup.html',
#                               {'error': 'user name already taken, please try different user name'})
#                 # now check is there any same user already created
#             except User.DoesNotExist:
#                 user = User.objects.create(username=request.POST['username'], password=request.POST['pass1'])
#                 auth.login(request, user)
#                 return redirect('products:home')
#         else:
#             return render(request, 'users/signup.html', {'error': 'Password UnMatch'})
#     else:
#         return render(request, 'users/signup.html')


def signup_v1(request):
    if request.method == 'POST':
        form = UserSignup(request.POST)
        if form.is_valid():
            user_obj = form.cleaned_data
            username = user_obj['username']  # i also can user user_obj.get('something'), and i think it's good
            email = user_obj['email']
            password = user_obj['password']

            User.objects.create_user(username, email, password)
            user = authenticate(username=username, password=password)
            print(username)
            auth.login(request, user)
            return redirect('products:home')

    else:
        form = UserSignup()
    return render(request, 'users/signup_v1.html', {'form': form})


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(request, username=request.POST['username'], password=request.POST['pass'])
        if user is not None:
            auth.login(request, user)
            return redirect('products:home')
        else:
            return render(request, 'users/login.html', {'error': 'Username or Password is incorrect'})
    else:
        return render(request, 'users/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('products:home')
