from rest_framework.test import APITestCase
import os
from unittest.mock import patch
from unittest.mock import ANY
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login

from core.models.resource import Resource, Image
from core.models.contributor import Contributor
from core.models.invitation import InvitationRequest


class TestUploadResourceApi(APITestCase):
    @classmethod
    def setUpTestData(cls):
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

class TestInvitationApi(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('invitation_api')
        cls.email = 'testemail@email.com'
        cls.payload = {'email': cls.email}
    def test_invitation_api_post_happy(self):
        response = self.client.post(self.url, self.payload)
        self.assertEqual(201, response.status_code)
    
    def test_happy_inv_creates_invittaion_request(self):
        response = self.client.post(self.url, self.payload)
        self.assertEqual(201, response.status_code)

        InvitationRequest.objects.filter(email=self.email)

    def test_happy_path_creates_event_log(self):
        log_patcher = patch('core.api.invitation.create_event_log')

        with log_patcher as log_mock:
            response = self.client.post(self.url, self.payload)
            self.assertEqual(201, response.status_code)
            log_mock.assert_called_once_with(action='invitation_api', 
                                             payload=ANY, status=201)

    def test_unhappy_path_empty_payload(self):
        response = self.client.post(self.url, {})
        self.assertEqual(400, response.status_code)

    def test_unhappy_path_wrong_payload_key(self):
        response = self.client.post(self.url, {'emails': 'emails'})
        self.assertEqual(400, response.status_code)
    
    def test_unhappy_creates_unhappy_log(self):
        log_patcher = patch('core.api.invitation.create_event_log')

        with log_patcher as log_mock:
            response = self.client.post(self.url, {'emails': 'bad_data'})
            self.assertEqual(400, response.status_code)
            log_mock.assert_called_once_with(action='invitation_api', 
                                             payload=ANY, status=400,
                                             error_details=ANY)


class TestContributorApi(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='Test')
        cls.contributor = Contributor.objects.create(
            user=cls.user
        )
        cls.url = reverse('contributor_api')

    def test_get_happy_path(self):
        payload = {'user_id': self.user.id}
        response = self.client.get(self.url, payload)
        self.assertEqual(200, response.status_code)
    
    def test_unhappy_get(self):
        payload = {'bad_key': ''}
        response = self.client.get(self.url, payload)
        self.assertEqual(400, response.status_code)