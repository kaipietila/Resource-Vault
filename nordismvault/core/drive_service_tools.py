
def create_new_drive_folder_with_additional_permissions(folder_name, email):
    if permisson_dict:
        permissions = drive_service.create_folder_permissions_for_email(email)
    folder_id = drive_service.create_folder(folder_name)
    drive_service.add_folder_permissions(permissions)

drive_service = DriveService()