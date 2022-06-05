from curses import ALL_MOUSE_EVENTS
from ssl import ALERT_DESCRIPTION_UNSUPPORTED_CERTIFICATE
from rest_framework import viewsets
from jobs.models import Job
from jobs.serializer import JobSerializer


class JobsViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.filter(active=True)
    serializer_class = JobSerializer