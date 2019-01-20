from django.db import models


class User(models.Model):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    reg_date = models.DateTimeField('registration_date')
    last_login_date = models.DateTimeField()

