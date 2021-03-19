from django.db import models
from django.contrib.auth.models import User
from time import ctime

class ApiEvent(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    payload = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    status = models.IntegerField()
    error_details = models.CharField(max_length=512, blank=True, null=True)
    action = models.CharField(max_length=255, blank=True)

    @property
    def readable_time(self):
        return self.create_time.ctime()

    def __str__(self):
        return (f'Event from {self.readable_time} with status {self.status}')
