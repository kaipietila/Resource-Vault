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
