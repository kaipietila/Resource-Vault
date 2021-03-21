from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.conf import settings

from core.models.resource import Resource, ResourceTag, Image
from drive.drive_service import get_drive_service
from core.models.event_log import ApiEvent


def create_resource(image, user):
    resource = Resource.objects.create(
        image=image,
        contributor=user.contributor,
    )
    return resource


def add_tags_to_resource(tags, resource):
    for tag in tags:
        tag, _ = ResourceTag.objects.get_or_create(tag=tag,)
        resource.tags.add(tag.id)


def create_image_and_upload_to_drive(uploaded_image, user):
    drive_service = get_drive_service()
    uploaded_image_drive_id = drive_service().upload_file(uploaded_image, user)
    image = Image.objects.create(
        name=uploaded_image.name,
        drive_id=uploaded_image_drive_id
    )
    return image


def get_user(user_id):
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        raise ValidationError('User does not exist')
    return user


def create_event_log(payload, status, action, error_details=None, user=None):
    ApiEvent.objects.create(
        payload=payload,
        user=user,
        status=status,
        error_details=error_details,
        action=action,
    )