from django.test import TestCase
from django.test import override_settings

from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import ANY
import os

from drive.drive_service import DriveService
from drive.drive_service import MockDriveService
from drive.drive_service import get_drive_service
from drive.drive_service import get_credentials
from drive.drive_service import DriveSetupError


class TestDriveService(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.file_to_upload = MagicMock()
        cls.file_to_upload.name.return_value = 'file_name.jpg'
        cls.user = MagicMock()
        cls.user.username = 'username'
        cls.user.__str__.return_value = 'test_user'
    
    def setUp(self):
        self.get_credentials_patcher = patch('drive.drive_service.get_credentials', 
                                      return_value='credentials')
        service_mock = MagicMock()
        self.google_build_patcher = patch('drive.drive_service.build', return_value=service_mock)
        self.mock_credentials = self.get_credentials_patcher.start()
        self.mock_build = self.google_build_patcher.start()
        
        self.drive_service = DriveService()

    def tearDown(self):
        self.get_credentials_patcher.stop()
        self.google_build_patcher.stop()
    
    def test_upload_file(self):
        patch_get_folder = patch('drive.drive_service.DriveService.get_or_create_folder', return_value=1)
        patch_upload = patch('drive.drive_service.DriveService.do_upload', return_value=1)
        patch_bytesio = patch('drive.drive_service.BytesIO', MagicMock())
        
        with patch_get_folder as folder_mock, patch_upload as upload_mock, patch_bytesio as byte_mock:
            upload_id = self.drive_service.upload_file(self.file_to_upload, self.user)
            folder_mock.assert_called_once_with(self.user)
            upload_mock.assert_called_once()
            byte_mock.assert_called_once()
        
        self.assertEqual(1, upload_id)


    def test_get_or_create_folder(self):
        create_folder_patch = patch('drive.drive_service.DriveService.create_folder', return_value=1)
        with create_folder_patch as create_mock:
            folder_id = self.drive_service.get_or_create_folder(self.user)
            create_mock.assert_called_once_with(self.user.username)
        self.assertEqual(1, folder_id)


    def test_create_folder_permissions_for_email(self):
        email = 'test@test.com'
        permission_dict = self.drive_service.create_folder_permissions_for_email(email)
        expected_permission_dict = {
            'type': 'user',
            'role': 'reader',
            "emailAddress": email,
        }
        self.assertEqual(expected_permission_dict, permission_dict)


class TestMockDriveService(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.service = MockDriveService()
        cls.file_to_upload = MagicMock()
        cls.file_to_upload.name.return_value = 'file_name'
        cls.user = MagicMock()
        cls.user.__str__.return_value = 'test_user'

    def test_mock_drive_upload(self):
        random_uploaded_file_id = self.service.upload_file(self.file_to_upload, self.user)
        self.assertTrue(random_uploaded_file_id)

class TestDriveSetupUtils(TestCase):

    @override_settings(USE_MOCK_SERVICE=True)
    def test_get_service_mock(self):
        service = get_drive_service()
        self.assertEqual(MockDriveService, service)
    
    @override_settings(USE_MOCK_SERVICE=False)
    def test_get_service_real_with_creds(self):
        service = get_drive_service()
        self.assertEqual(DriveService, service)

    def test_get_credentials(self):
        creds_path_patcher = patch('drive.drive_service.get_credentials_path', return_value='path')
        google_service_account_patch = patch('google.oauth2.service_account.Credentials.from_service_account_file', 
                                             return_value='creds')
        with creds_path_patcher as creds_path_mock, google_service_account_patch as google_mock:
            credentials = get_credentials()
            creds_path_mock.assert_called_once()
            google_mock.assert_called_once_with('path', scopes=ANY)
        self.assertEqual('creds', credentials)
