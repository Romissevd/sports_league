from django.db import models


class FCStadium(models.Model):

    stadium_name = models.CharField(max_length=200, default='')
    city = models.CharField(max_length=200, default='')
    capacity = models.IntegerField(default=0)
    url_stadium = models.URLField(default='')


class CountryRuName(models.Model):

    country_name = models.CharField(max_length=50)


class League(models.Model):

    league_name = models.CharField(max_length=100)


class DictionaryClubName(models.Model):

    club_name = models.CharField(max_length=200)


class ParsingData(models.Model):

    name_id = models.IntegerField(default=0)
    link_for_parsing = models.URLField(default='')
    country_id = models.IntegerField(default=0)
    league_id = models.IntegerField(default=0)


class FootballClub(models.Model):

    fc_en_name = models.CharField(max_length=200, default='')
    num_image = models.IntegerField(default=0)
    date_of_foundation = models.DateField(null=True)
    address = models.CharField(max_length=200, default='')
    country = models.ForeignKey(CountryRuName, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200, default='')
    fax = models.CharField(max_length=200, default='')
    email = models.EmailField(default='')
    site = models.URLField(default='')
    stadium = models.ForeignKey(FCStadium, on_delete=models.CASCADE)
