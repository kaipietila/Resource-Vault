from django.test import TestCase
from django.contrib.auth.models import User

from unittest.mock import Mock, patch
from waffle.testutils import override_switch
import pytest

from core.models.contributor import Contributor
from core.models.resource import Resource
from core.utils import create_resource
from core.models.resource import Image
from core.utils import update_resource_description
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

    def test_update_resource_description(self):
        self.assertEqual('', self.resource.description)
        description = 'description'
        update_resource_description(description, self.resource)

        self.assertEqual(description, self.resource.description)
    
    def test_add_tags_to_resource(self):
        tag_list = ['one', 'two', 'three',]
        add_tags_to_resource(tag_list, self.resource)

        self.assertEqual(3, len(self.resource.tags.all()))
