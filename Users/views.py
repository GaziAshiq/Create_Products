from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth


# Create your views here.
def signup(request):
    # TODO there is a bug. user can sign up successfully, but django not using hashing for password. so when new user
    #  try to login, it throw an error, because password hashing algorithm not working. i have to look at it

    if request.method == 'POST':
        if request.POST['pass1'] == request.POST['pass2']:  # if both password match
            print(request.POST['pass1'])
            try:
                user = User.objects.get(username=request.POST['username'])
                user.set_unusable_password()
                user.save()
                return render(request, 'users/signup.html',
                              {'error': 'user name already taken, please try different user name'})
                # now check is there any same user already created
            except User.DoesNotExist:
                user = User.objects.create(username=request.POST['username'], password=request.POST['pass1'])
                auth.login(request, user)
                return redirect('products:home')
        else:
            return render(request, 'users/signup.html', {'error': 'Password UnMatch'})
    else:
        return render(request, 'users/signup.html')


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
