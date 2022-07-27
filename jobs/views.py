from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from jobs.models import Job
from jobs.pagination import CustomJobsResultsSetPagination
from jobs.serializer import JobSerializer


class JobsViewSet(viewsets.ModelViewSet):
    # queryset = Job.objects.filter(active=True).order_by('-date')
    serializer_class = JobSerializer
    permission_classes = (AllowAny,)
    pagination_class = CustomJobsResultsSetPagination

    def get_queryset(self):
        queryset = Job.objects.filter(active=True).order_by("-date")
        company = self.request.query_params.get("company")
        remote = self.request.query_params.get("remote")

        if company:
            queryset = queryset.filter(company=company)

        if remote == "true":
            queryset = queryset.filter(remote=True)
        if remote == "false":
            queryset = queryset.filter(remote=False)

        return queryset
