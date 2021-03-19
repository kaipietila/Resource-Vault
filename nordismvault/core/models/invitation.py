from django.db import models

class InvitationRequest(models.Model):
    email = models.CharField(max_length=128)
    create_time = models.DateTimeField(auto_now_add=True)
    invited = models.BooleanField(default=False)

    def __str__(self):
        return(f'Invitation request from {self.email}')