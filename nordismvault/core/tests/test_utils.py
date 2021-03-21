from django.test import TestCase
from django.contrib.auth.models import User
from django.test import override_settings

from unittest.mock import MagicMock

from core.models.contributor import Contributor
from core.models.resource import Resource
from core.utils import create_resource
from core.models.resource import Image
from core.utils import add_tags_to_resource
from core.utils import create_image_and_upload_to_drive


class TestUtils(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.img = Image.objects.create(
            drive_id='test_id',
            name='name',
        )
        cls.user = User.objects.create_user(
            username='test', email='admin@admin', password='top_secret')
        cls.contributor = Contributor.objects.create(
            user=cls.user,
        )
        cls.resource = Resource.objects.create(
            image=cls.img,
            contributor=cls.contributor,
        )

    def test_create_resource(self):
        resource = create_resource(self.img, self.user)

        self.assertEqual(resource.image, self.img)
        self.assertEqual(resource.contributor, self.contributor)
    
    @override_settings(USE_MOCK_SERVICE=True)
    def test_create_image_and_upload_to_drive(self):
        image_file = MagicMock()
        image_file.name = 'image'

        image = create_image_and_upload_to_drive(image_file, self.user)
        self.assertEqual('image', image.name)
