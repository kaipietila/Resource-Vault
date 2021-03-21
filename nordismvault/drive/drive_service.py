from __future__ import print_function
import os.path
import mimetypes
from io import BytesIO
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

class DriveSetupError(Exception):
    pass


class DriveService(object):
    def __init__(self):
        credentials = get_credentials()
        self.service = build('drive', 'v3', credentials=credentials)

    def upload_file(self, file_to_upload, user):
        folder_id = self.get_or_create_folder(user)
        file_name = file_to_upload.name
        mime_type, _ = mimetypes.guess_type(file_name)
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        byte_file = BytesIO(file_to_upload.read())
        response_id = self.do_upload(byte_file, mime_type)
        return response_id
    
    def do_upload(byte_file, mime_type):
        media = MediaIoBaseUpload(fh, mimetype=mime_type, chunksize=1024 * 1024, resumable=True)
        response = self.service.files().create(
            body=file_metadata, media_body=media, fields='id').execute()
        return response['id']
    
    def get_or_create_folder(self, user):
        if settings.USE_TEST_DRIVE_FOLDER:
            folder_id = TEST_FOLDER_ID
        # folders are created with the username of the uploader
        folder_id = self.create_folder(user.username)
        return folder_id

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


class MockDriveService(object):

    def upload_file(self, file, user):
        mock_id = random.randint(1,10000)
        print(f"File: {file.name} uploaded to Drive for user {user}. Image id: {mock_id}")
        return mock_id
    
    def get_files(self):
        return ''
    
    def create_folder_permissions_for_email(self, email):
        user_permission = {
            'type': 'user',
            'role': 'reader',
            "emailAddress": email,
        }
        return user_permission
    
    def add_folder_permissions(self, folder_id, permission_dict):
        return
    
    def create_folder(self, folder_name):
        return random.randint(0,100)


def get_drive_service():
    if settings.USE_MOCK_SERVICE:
        service = MockDriveService
    else:
        service = DriveService
    return service  

def get_credentials():
    try:
        path_to_creds = get_credentials_path()
    except FileNotFoundError:
        raise DriveSetupError('Credentials file not properly setup')
    creds = service_account.Credentials.from_service_account_file(
        path_to_creds, scopes=SCOPES)
    return creds

def get_credentials_path():
    path_to_creds = os.path.join(os.path.dirname(__file__), 
                                     settings.DRIVE_CREDENTIALS_FILE_NAME)
    return path_to_creds