from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect, render

from core.models.contributor import Contributor
from core.utils import create_event_log

VERIFICATION_REQUIRED_MESSAGE = 'Please wait while your account is being verified'
INVALID_CREDENTIALS = 'Your username or password did not match. Try again!'


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.contributor.is_verified():
                messages.error(request, VERIFICATION_REQUIRED_MESSAGE)
                create_event_log(payload=form.data, action='login_view', 
                                user=user, status=400, error_details='Contributor not verified')
                return redirect('login_user')
            create_event_log(payload=form.data, action='login_view', 
                            user=user, status=200)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, INVALID_CREDENTIALS)
            create_event_log(payload=form.data, action='login_view', 
                             status=400, error_details='User credentials do not match')
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
