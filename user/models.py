from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_avatar = models.ImageField(upload_to='avatar')
    gender = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    about_me = models.CharField(max_length=1000, blank=True, default='')
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{first_name} {last_name}'.format(
            first_name=self.user.first_name,
            last_name=self.user.last_name,
        )
