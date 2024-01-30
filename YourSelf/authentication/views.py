from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

from .forms import CreateUserForm
from django.contrib import auth

def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = UserCreationForm()
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'registration_form.html', context)

def login_page(request):
    context = {}
    return render(request, 'login.html', context)


def profile_view(request):
    return render(request, 'profile.html')

def logout(request):
    auth.logout(request)
    return redirect("home")