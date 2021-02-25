from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import  HttpResponse
from django.shortcuts import render, redirect

from core.drive_service import DriveService
from core.forms import ResourceForm
from core.models.resource import Resource, ResourceTag, Image


def create_resource_and_tags(data, image):
    user = User.objects.get(id=data['user'])
    resource = Resource.objects.create(
        image=image,
        contributor=user.contributor,
        description=data['description'],
    )
    tag_names = data['tags'].split(',')
    for tag_name in tag_names:
        tag, _ = ResourceTag.objects.get_or_create(
            tag=tag_name,
        )
        resource.tags.add(tag.id)


def create_image_and_upload_to_drive(file):
    uploaded_file_id = DriveService().upload_file(file)
    image = Image.objects.create(
                name=file.name,
                drive_id=uploaded_file_id
            )

    return image


@login_required
def add_resource_view(request):
    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            image = create_image_and_upload_to_drive(request.FILES['image'])
            create_resource_and_tags(form.cleaned_data, image)
            return redirect('core-success')

    else:
        form = ResourceForm(initial={'user': request.user.id})
    return render(request, 'add_resource.html', {'form': form})


def success_view(request):
    return HttpResponse('<h1>Success!</h1>')


def error_view(request):
    return HttpResponse('<h1>Error! Try again soon!</h1>')