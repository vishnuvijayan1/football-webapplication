from django.db import models


class Teams(models.Model):
    team_name = models.CharField(max_length=250)
    team_players = models.CharField(max_length=1000)
    team_coach = models.CharField(max_length=250)
    team_manager = models.CharField(max_length=250)


class TeamMatches(models.Model):
    team_a = models.ForeignKey(
        Teams, on_delete=models.CASCADE, null=False, blank=False)
    team_b = models.ForeignKey(
        Teams, on_delete=models.CASCADE, null=False, blank=False, related_name='teamb')
    venue = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    team_a_points = models.IntegerField(null=True)
    team_b_points = models.IntegerField(null=True)