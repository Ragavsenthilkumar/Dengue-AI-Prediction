from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CitizenRegisterForm


def register_view(request):
    """Citizen registration."""
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    if request.method == 'POST':
        form = CitizenRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('dashboard:index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CitizenRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Login for both citizens and officers."""
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect officers to dashboard, citizens to home
                if hasattr(user, 'profile') and user.profile.is_officer:
                    messages.success(request, f'Welcome back, Officer {username}!')
                    return redirect('dashboard:dashboard-home')
                else:
                    messages.success(request, f'Welcome back, {username}!')
                    return redirect('dashboard:index')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Logout and redirect to home."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('dashboard:index')
