from django.db import models


# class FCStadium(models.Model):
#
#     name = models.CharField(max_length=200, default='')
#     city = models.CharField(max_length=200, default='')
#     capacity = models.IntegerField(default=0)


class CountryRuName(models.Model):

    country_name = models.CharField(max_length=50)


class League(models.Model):

    league_name = models.CharField(max_length=100)


class DictionaryClubName(models.Model):

    en_name = models.CharField(max_length=200)
    ru_name = models.CharField(max_length=200, default='')


class ParsingData(models.Model):

    name = models.OneToOneField(DictionaryClubName, on_delete=models.CASCADE)
    link_for_parsing = models.URLField(default='')
    country = models.ForeignKey(CountryRuName, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)


# class FootballClub(models.Model):
#
#     name = models.OneToOneField(DictionaryClubName, on_delete=models.CASCADE)
#     id_image = models.IntegerField(default=0)
#     year_of_foundation = models.DateField(null=True)
#     address = models.CharField(max_length=200, default='')
#     country = models.ForeignKey(CountryRuName, on_delete=models.CASCADE)
#     phone = models.CharField(max_length=200, default='')
#     fax = models.CharField(max_length=200, default='')
#     email = models.EmailField(default='')
#     site = models.URLField(default='')
#     stadium = models.ForeignKey(FCStadium, on_delete=models.CASCADE)
