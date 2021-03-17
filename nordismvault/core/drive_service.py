from __future__ import print_function
import os.path
import mimetypes
from io import BytesIO
import waffle

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


class DriveService(object):
    def __init__(self):
        self.get_service = self.get_service()

    def get_service(self):
        if settings.PATH_TO_DRIVE_CREDENTIALS_FILE:
            credentials = service_account.Credentials.from_service_account_file(
                path_to_file, scopes=SCOPES)
            service = build('drive', 'v3', credentials=credentials)
        else:
            service = MockDriveService()
        return service

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
        response = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return response['id']
    
    def get_or_create_folder(self, user):
        if not waffle.switch_is_active(USE_REAL_DRIVE_FOLDERS):
            return TEST_FOLDER_ID
        # folders are created with the username of the uploader
        folder = self.create_folder(user.username)

    def create_folder(self, folder_name):
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = self.service.files().create(
            body=folder_metadata,
        ).execute()
    
    def add_folder_permissions(self, permission_dict, folder_id)
        self.service.permissions().create(
            fileId=folder_id,
            body=permission_dict,
        ).execute()

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
