from django.db import models


class Company(models.Model):
    url = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=250)
    linkedin = models.CharField(max_length=250, blank=True, null=True, default=None)
    website = models.CharField(max_length=250, blank=True, null=True, default=None)
    glassdoor = models.CharField(max_length=250, blank=True, null=True, default=None)
    logo = models.BinaryField(blank=True, null=True, default=None)

    def __str__(self):
        return self.name
