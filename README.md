# Nordism Resource Vault
DEMO for a file vault to store resources for Nordism projects.

Using Google drive API to store images in google service account drive.
If you want to use driev you need to provide service account credentials file
to the project and set in settings PATH_TO_DRIVE_CREDENTIALS_FILE as the path to 
your credentials file.

Also if you want to use upload files to drive disable USE_MOCK_SERVICE.

To setup run:
docker-compose build nordismvault

docker-compose up

Run migrations:
docker-compose exec nordismvault bash
python manage.py migrate

Create user:
python manage.py createsuperuser

access admin at localhost:8000/admin
You need to verify your user to be able to log in

Go to contributor and "Add Contributor" 
Select you user and add. Also check the Verify button

The you can login from 
localhost:8000

