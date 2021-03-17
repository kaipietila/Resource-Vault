from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError

from core.drive_service import DriveService
from core.forms import ResourceForm
from core.models.resource import Resource, ResourceTag, Image
from core.utils import create_resource_and_tags
from core.utils import create_image_and_upload_to_drive
from core.utils import get_user


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
