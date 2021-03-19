from rest_framework.test import APITestCase
import os
from unittest.mock import patch
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login

from core.models.resource import Resource, Image
from core.models.contributor import Contributor


class TestUploadResourceApi(APITestCase):
    @classmethod
    def setUpTestData(cls):
        path_to_file = os.path.join(os.path.dirname(__file__), 'fixtures', 'text.txt')
        cls.uploaded_file = open(path_to_file, 'r', encoding='utf-8')
        cls.payload = {
            'file': 'test'
        }
        cls.upload_api_url = reverse('upload_resource_api')

    def test_upload_resource_api_post_fail(self):
        upload_patcher = patch('core.api.resource.create_image_and_upload_to_drive')
        resource_patcher = patch('core.api.resource.create_resource')
        with upload_patcher as upload_mock, resource_patcher as create_res_mock:
            response = self.client.post(self.upload_api_url, data={})
            self.assertEqual(400, response.status_code)

    def test_upload_resource_api_get_not_allowed(self):
        upload_patcher = patch('core.api.resource.create_image_and_upload_to_drive')
        resource_patcher = patch('core.api.resource.create_resource')
        with upload_patcher as upload_mock, resource_patcher as create_res_mock:
            response = self.client.get(self.upload_api_url)
            self.assertEqual(405, response.status_code)
