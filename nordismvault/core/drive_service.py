from __future__ import print_function
import os.path
import mimetypes
from io import BytesIO
import waffle
import random

from django.conf import settings

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload


SCOPES = ['https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive.metadata',
          ]

TEST_FOLDER_ID = "16G1GcrqqbQDC2NuyKDY35zb9hRe-dRdi"
USE_REAL_DRIVE_FOLDERS = 'use_real_drive_folders'
USE_MOCK_SERVICE = 'use_mock_service'


def get_drive_service():
    if (settings.PATH_TO_DRIVE_CREDENTIALS_FILE 
        and not waffle.switch_is_active('USE_MOCK_SERVICE')):
        credentials = service_account.Credentials.from_service_account_file(
            settings.PATH_TO_DRIVE_CREDENTIALS_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)
    else:
        service = MockDriveService()
    return service


class BaseDriveService(object):
     def __init__(self):
        self.service = get_drive_service()

class DriveService(BaseDriveService):
    def upload_file(self, file, user):
        folder_id = self.get_or_create_folder(user)
        file_name = file.name
        mime_type, _ = mimetypes.guess_type(file_name)
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        fh = BytesIO(file.read())
        media = MediaIoBaseUpload(fh,
                                  mimetype=mime_type,
                                  chunksize=1024 * 1024,
                                  resumable=True)
        response = self.service.files().create(
            body=file_metadata, media_body=media, fields='id').execute()
        return response['id']
    
    def get_or_create_folder(self, user):
        if not waffle.switch_is_active(USE_REAL_DRIVE_FOLDERS):
            return TEST_FOLDER_ID
        # folders are created with the username of the uploader
        return self.create_folder(user.username)

    def create_folder(self, folder_name):
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder_id = self.service.files().create(
            body=folder_metadata).execute()
        return folder_id
    
    def add_folder_permissions(self, folder_id, permission_dict):
        self.service.permissions().create(
            fileId=folder_id, body=permission_dict).execute()

    def get_files(self):
        response = self.service.files().list().execute()
        return response.get('files', [])
    
    def create_folder_permissions_for_email(self, email):
        user_permission = {
            'type': 'user',
            'role': 'reader',
            "emailAddress": email,
        }
        return user_permission


class MockDriveService(BaseDriveService):

    def upload_file(self, file, user):
        mock_id = random.randint(1,10000)
        print(f"File: {file.name} uploaded to Drive for user {user}. Image id: {mock_id}")
        return mock_id
    