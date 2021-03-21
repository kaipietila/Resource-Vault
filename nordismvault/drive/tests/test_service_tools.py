from django.test import TestCase
from django.test import override_settings
from unittest.mock import patch

from drive.drive_service import MockDriveService
from drive.drive_service_tools import create_new_drive_folder_with_additional_permissions
from drive.drive_service_tools import get_all_files

@override_settings(USE_MOCK_SERVICE=False)
class TestDriveServiceTools(TestCase):

    def test_create_new_drive_folder_with_additional_permissions(self):
        create_permissions_patcher = patch('drive.drive_service.DriveService.create_folder_permissions_for_email')
        create_folder_patcher = patch('drive.drive_service.DriveService.create_folder', return_value=1)
        add_permissions_patcher = patch('drive.drive_service.DriveService.add_folder_permissions')

        with (create_folder_patcher as create_folder_mock, 
              create_permissions_patcher as create_perms_mock,
              add_permissions_patcher as add_perms_mock):
            folder_id = create_new_drive_folder_with_additional_permissions('folder_name', 'email')
            create_folder_mock.assert_called_once()
            create_perms_mock.assert_called_once()
            add_perms_mock.assert_called_once()
        self.assertEqual(1, folder_id)

    def test_create_new_drive_folder_with_additional_permissions__without_email(self):
        # if the function is called without email we wont create permissions and add them 
        create_folder_patcher = patch('drive.drive_service.DriveService.create_folder', return_value=1)

        with create_folder_patcher as create_folder_mock:
            folder_id = create_new_drive_folder_with_additional_permissions('folder_name')
            create_folder_mock.assert_called_once()
        self.assertEqual(1, folder_id)

    def test_get_all_files(self):
        get_files_patcher = patch('drive.drive_service.DriveService.get_files')

        with get_files_patcher as get_files_mock:
            get_all_files()
            get_files_mock.assert_called_once()
            