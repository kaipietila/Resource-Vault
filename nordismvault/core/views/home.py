
from django.shortcuts import render, redirect

from core.models.contributor import Contributor
from core.models.resource import Resource


def home(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    contributor = Contributor.objects.get(user=request.user)
    resources = Resource.objects.filter(contributor=contributor)
    context = {
        'contributor': contributor,
        'resources': resources,
    }
    return render(request, 'home.html', context)

