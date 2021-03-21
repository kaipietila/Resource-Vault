from django.test import TestCase
from django.contrib.auth.models import User

from core.models.contributor import Contributor
from core.models.resource import Resource
from core.models.resource import Image


class TestResourceMethods(TestCase):
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

    def test_add_tags(self):
        tag_list = ['one', 'two', 'three',]
        self.resource.add_tags(tag_list)

        self.assertEqual(3, len(self.resource.tags.all()))

    def test_update_description(self):
        self.resource.update_description('new_description')

        self.assertEqual('new_description', self.resource.description)
