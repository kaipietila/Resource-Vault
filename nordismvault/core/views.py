from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from core.forms import ResourceForm

from core.models.contributor import Contributor
from core.models.resource import Resource, ResourceTag


def create_resource_and_tags(data):
    try:
        contributor = Contributor.objects.get(id=data['contributor_id'])
    except ObjectDoesNotExist:
        raise ValidationError('Contributor not found')

    resource = Resource.objects.create(
        file=data['file'],
        contributor=contributor,
        description=data['description'],
    )
    tag_names = data['tags'].split()
    for name in tag_names:
        tag = ResourceTag.objects.get_or_create(
            tag=name,
        )
        resource.tags.add(tag)


def add_resource_view(request):
    if request.method == "POST":
        form = ResourceForm(request.POST)
        if form.is_valid():
            try:
                create_resource_and_tags(form.cleaned_data)
            except ValidationError:
                return HttpResponseRedirect('core-error')
            return HttpResponseRedirect('core-success')
    else:
        form = ResourceForm()

    return render(request, 'core-add-resource', {'form': form})


def success_view(request):
    return HttpResponse('<h1>Success!</h1>')


def error_view(request):
    return HttpResponse('<h1>Error! Try again soon!</h1>')