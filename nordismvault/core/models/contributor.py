from django.db import models
from django.contrib.auth.models import User


class Contributor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='contributor')
    verified = models.BooleanField(default=False)

    def is_verified(self):
        return self.verified