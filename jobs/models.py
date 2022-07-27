from django.db import models
import datetime
from companies.models import Company


class Job(models.Model):
    url = models.CharField(max_length=255, unique=True, primary_key=True)
    title = models.CharField(max_length=250)
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)
    remote = models.BooleanField(default=None)
    location = models.CharField(max_length=250, default=None)
    date = models.DateField(blank=True, null=True, default=datetime.date.today)
    seniority = models.CharField(null=True, max_length=40, default=None)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title
