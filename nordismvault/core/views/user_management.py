from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect, render

from core.models.contributor import Contributor

VERIFICATION_REQUIRED_MESSAGE = 'Please wait while your account is being verified'


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.contributor.is_verified():
                login(request, user)
                return redirect('core-add-resource')
            else:
                messages.add_message(request, messages.INFO, VERIFICATION_REQUIRED_MESSAGE)
                return redirect('home')
        else:
            return redirect('home')
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


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
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
