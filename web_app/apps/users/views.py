from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomRegistrationForm, UserEditForm, PlayerProfileForm
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


@login_required
def edit_profile(request):
    profile, created = PlayerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = PlayerProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, "Profile updated successfully!")

            return redirect('profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = PlayerProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()

        messages.success(request, "Your account has been deleted.")

        return redirect("home")

    return redirect('profile')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'users/change_password.html', {
        'form': form
    })
