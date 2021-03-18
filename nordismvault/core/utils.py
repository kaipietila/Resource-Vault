from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from core.models.resource import Resource, ResourceTag, Image
from core.drive_service import DriveService


def create_resource(image, user):
    resource = Resource.objects.create(
        image=image,
        contributor=user.contributor,
    )
    return resource


def update_resource_description(description, resource):
    resource.description = description
    resource.save(updated_fields=['description'])


def add_tags_to_resource(tags, resource):
    for tag in tags:
        tag, _ = ResourceTag.objects.get_or_create(
            tag=tag,
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
