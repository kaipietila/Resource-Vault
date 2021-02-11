# Service used to upload files with google drive api
from __future__ import print_function
import os.path
import mimetypes
from io import BytesIO

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload


SCOPES = ['https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive.metadata',
          ]

path_to_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                            'credentials', 'resource-vault-key.json')


class DriveService(object):
    def __init__(self):
           credentials = service_account.Credentials.from_service_account_file(
               path_to_file, scopes=SCOPES)
           self.service = build('drive', 'v3', credentials=credentials)

    def upload_file(self, file, folder_id='16G1GcrqqbQDC2NuyKDY35zb9hRe-dRdi'):
        # 16G1GcrqqbQDC2NuyKDY35zb9hRe-dRdi test-folder
        folder_id = folder_id
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

    def create_folder(self):
        folder_metadata = {
            'name': 'test folder',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = self.service.files().create(
            body=folder_metadata,
        ).execute()
        user_permission = {
            'type': 'user',
            'role': 'reader',
            "emailAddress": 'kai.pietila1@gmail.com',
        }
        self.service.permissions().create(
            fileId=folder['id'],
            body=user_permission,
        ).execute()
        return folder['id']

    def get_files(self):
        response = self.service.files().list().execute()
        return response.get('files', [])
