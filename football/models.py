from django.db import models


class FCStadium(models.Model):

    name = models.CharField(max_length=200, default='')
    city = models.CharField(max_length=200, default='')
    capacity = models.IntegerField(default=0)


class FootballClub(models.Model):

    eng_name = models.CharField(max_length=200)
    ru_name = models.CharField(max_length=200)
    id_image = models.IntegerField(default=0)
    year_of_foundation = models.DateField(null=True)
    address = models.CharField(max_length=200, default='')
    country = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, default='')
    fax = models.CharField(max_length=200, default='')
    email = models.EmailField(default='')
    stadium = models.ForeignKey(FCStadium, on_delete=models.CASCADE)
