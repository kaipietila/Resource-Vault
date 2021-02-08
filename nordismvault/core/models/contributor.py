from django.db import models


class Contributor(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField()
    create_time = models.DateTimeField(auto_now_add=True)
