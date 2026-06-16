from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomRegistrationForm
from .models import PlayerProfile

# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('dashboard')

    else:
        form = CustomRegistrationForm()

    return render(request, 'users/register.html', {
        'form': form
    })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('dashboard')

    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {
        'form': form
    })


def logout_view(request):
    logout(request)

    return redirect('home')


@login_required
def profile_view(request):
    profile, created = PlayerProfile.objects.get_or_create(user=request.user)

    return render(request, 'users/profile.html', {
        'profile': profile
    })
