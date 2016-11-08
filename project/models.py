from django.db import models
from django.utils import timezone

#project model
class Project(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    about = models.TextField()
    total_fund = models.IntegerField(default=0)
    created_date = models.DateTimeField(
            default=timezone.now)
    
#match model - match project with funders who wants to fund
class Match(models.Model):
    project = models.ForeignKey(Project)
    funder = models.ForeignKey('auth.User')
    funding = models.IntegerField()

