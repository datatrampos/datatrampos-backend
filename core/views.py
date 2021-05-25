from rest_framework import generics

from .models import Job
from .serializers import JobSerializer


class ListJobView(generics.ListAPIView):
    queryset = Job.objects.all()  # used for returning objects from this view
    serializer_class = JobSerializer
