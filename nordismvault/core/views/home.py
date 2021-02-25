from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models.contributor import Contributor
from core.models.resource import Resource


@login_required
def home(request):
    contributor = Contributor.objects.get(user=request.user)
    resources = Resource.objects.filter(contributor=contributor)
    context = {
        'contributor': contributor,
        'resources': resources,
    }
    return render(request, 'home.html', context)

