from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from core.forms import ResourceForm
from core.utils import create_resource, update_resource_description
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
                resource = create_resource(form.cleaned_data, image, user)
                update_resource_description(form.cleaned_data['description'], resource)
                return redirect('home')
            except ValidationError as e:
                render(request, 'add_resource.html', {'non_field_errors': e.message})
    else:
        form = ResourceForm(initial={'user': request.user.id})
    return render(request, 'add_resource.html', {'form': form})
