from django.contrib.postgres.fields import JSONField
from django.db import models
from datetime import datetime


class FCStadium(models.Model):

    stadium_name = models.CharField(max_length=200, default='')
    city = models.CharField(max_length=200, default='')
    capacity = models.IntegerField(default=0)
    url_stadium = models.URLField(default='')


class CountryRuName(models.Model):

    country_name = models.CharField(max_length=50)


class CountryEnName(models.Model):

    country_name = models.CharField(max_length=50)
    ru_name = models.ForeignKey(CountryRuName, on_delete=models.CASCADE)


class League(models.Model):

    league_name = models.CharField(max_length=100)


class DictionaryClubName(models.Model):

    club_name = models.CharField(max_length=200)


class ParsingData(models.Model):

    name_id = models.ForeignKey(DictionaryClubName, on_delete=models.CASCADE)
    link_for_parsing = models.URLField(default='')
    country_id = models.ForeignKey(CountryRuName, on_delete=models.CASCADE)
    league_id = models.ForeignKey(League, on_delete=models.CASCADE)


class FootballClub(models.Model):

    fc_en_name = models.CharField(max_length=200, default='')
    alt_name = models.CharField(max_length=200, default='')
    fc_id_name_dictionary = models.ForeignKey(DictionaryClubName, on_delete=models.CASCADE)
    num_image = models.IntegerField(default=0)
    year_of_foundation = models.IntegerField(default=0)
    address = models.CharField(max_length=200, default='')
    country = models.ForeignKey(CountryRuName, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200, default='')
    fax = models.CharField(max_length=200, default='')
    email = models.EmailField(default='')
    site = models.URLField(default='')
    stadium = models.ForeignKey(FCStadium, on_delete=models.CASCADE)


class APIChampionsLeague(models.Model):

    date = models.DateTimeField()
    data = JSONField()


class ChampionsLeagueGroupStage(models.Model):

    team = models.ForeignKey(FootballClub, on_delete=models.CASCADE)
    groups = models.CharField(max_length=1, default='')
    position = models.IntegerField()
    points = models.IntegerField()
    played_games = models.IntegerField()
    won = models.IntegerField()
    draw = models.IntegerField()
    lost = models.IntegerField()
    goals_difference = models.IntegerField()
    goals_against = models.IntegerField()
    goals_for = models.IntegerField()
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    last_update = models.DateTimeField(default=datetime.now())


class ChampionsLeagueMatches(models.Model):

    home_team = models.ForeignKey(FootballClub, on_delete=models.CASCADE, related_name='home')
    away_team = models.ForeignKey(FootballClub, on_delete=models.CASCADE, related_name='away')
    groups = models.CharField(max_length=50, null=True)
    stage = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    time_match = models.DateTimeField(default=datetime.now())
    away_team_extratime = models.IntegerField(null=True)
    home_team_extratime = models.IntegerField(null=True)
    away_team_fulltime = models.IntegerField(null=True)
    home_team_fulltime = models.IntegerField(null=True)
    away_team_halftime = models.IntegerField(null=True)
    home_team_halftime = models.IntegerField(null=True)
    away_team_penalties = models.IntegerField(null=True)
    home_team_penalties = models.IntegerField(null=True)
    winner = models.CharField(max_length=50, null=True)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    last_updated = models.DateTimeField(default=datetime.now())


class APIMatches(models.Model):

    date = models.DateTimeField()
    league_code = models.CharField(max_length=10)
    data = JSONField()


class CodeLeague(models.Model):

    league_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    league = models.ForeignKey(League, on_delete=models.CASCADE)


class APITables(models.Model):

    date = models.DateTimeField()
    league_code = models.CharField(max_length=10)
    tables = JSONField()
