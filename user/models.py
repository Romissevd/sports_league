from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pol = models.CharField(max_length=2)

    def __str__(self):
        return '{first_name} {last_name}'.format(
            first_name=self.user.first_name,
            last_name=self.user.last_name,
        )
