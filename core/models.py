from django.db import models


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=25)
    job_title = models.CharField(max_length=50)
    url = models.CharField(max_length=70)
    remote = models.CharField(max_length=6)
    workplace = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self):
        return self.company_name
