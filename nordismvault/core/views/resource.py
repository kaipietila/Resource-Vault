from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError

from core.drive_service import DriveService
from core.forms import ResourceForm
from core.models.resource import Resource, ResourceTag, Image


def create_resource_and_tags(data, image, user):
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


def create_image_and_upload_to_drive(file, user):
    uploaded_file_id = DriveService().upload_file(file, user)
    image = Image.objects.create(
                name=file.name,
                drive_id=uploaded_file_id
            )

    return image

def get_user(user_id):
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        raise ValidationError('User does not exist')
    return user

@login_required
def add_resource_view(request):
    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = get_user(form.cleaned_data['user'])
                image = create_image_and_upload_to_drive(request.FILES['image'], user)
                create_resource_and_tags(form.cleaned_data, image, user)
                return redirect('home')
            except ValidationError as e:
                render(request, 'add_resource.html', {'non_field_errors': e.message})
    else:
        form = ResourceForm(initial={'user': request.user.id})
    return render(request, 'add_resource.html', {'form': form})
