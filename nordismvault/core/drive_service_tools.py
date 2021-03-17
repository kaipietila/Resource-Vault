from core.drive_service import DriveService


def create_new_drive_folder_with_additional_permissions(folder_name, email):
    if email:
        permissions = drive_service.create_folder_permissions_for_email(email)
    folder_id = drive_service.create_folder(folder_name)
    if permissions:
        drive_service.add_folder_permissions(folder_id=folder_id, permission_dict=permissions)
    return folder_id

def get_all_files():
    drive_service.get_files()

drive_service = DriveService()