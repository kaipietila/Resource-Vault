from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect, render

from core.models.contributor import Contributor

VERIFICATION_REQUIRED_MESSAGE = 'Please wait while your account is being verified'
INVALID_CREDENTIALS = 'Your username or password did not match. Try again!'


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.contributor.is_verified():
                messages.error(request, VERIFICATION_REQUIRED_MESSAGE)
                return redirect('login_user')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, INVALID_CREDENTIALS)
            return redirect('login_user')
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login_user')


def create_contributor(user):
    Contributor.objects.create(
        user=user
    )


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            create_contributor(user)
            return redirect('login_user')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
