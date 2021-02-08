from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from core.forms import ResourceForm

from core.models.contributor import Contributor
from core.models.resource import Resource, ResourceTag, Image


def create_resource_and_tags(data, image):
    try:
        contributor = Contributor.objects.get(id=data['contributor_id'])
    except ObjectDoesNotExist:
        raise ValidationError('Contributor not found')

    resource = Resource.objects.create(
        image=image,
        contributor=contributor,
        description=data['description'],
    )
    tag_names = data['tags'].split(',')
    for tag_name in tag_names:
        tag, _ = ResourceTag.objects.get_or_create(
            tag=tag_name,
        )
        resource.tags.add(tag.id)


def add_resource_view(request):
    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            image = Image(file=request.FILES['image'])
            image.save()
            try:
                create_resource_and_tags(form.cleaned_data, image)
            except ValidationError:
                return redirect('core-error')
            return redirect('core-success')
    else:
        form = ResourceForm()

    return render(request, 'add_resource.html', {'form': form})


def success_view(request):
    return HttpResponse('<h1>Success!</h1>')


def error_view(request):
    return HttpResponse('<h1>Error! Try again soon!</h1>')