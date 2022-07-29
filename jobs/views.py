from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from jobs.models import Job
from jobs.serializer import JobSerializer
from jobs.pagination import CustomJobsResultsSetPagination


class JobsViewSet(viewsets.ModelViewSet):
    # queryset = Job.objects.filter(active=True)
    serializer_class = JobSerializer
    permission_classes = (AllowAny,)
    pagination_class = CustomJobsResultsSetPagination

    def get_queryset(self):
        queryset = Job.objects.filter(active=True)
        company = self.request.query_params.get("company")
        remote = self.request.query_params.get("remote")
        order_by = self.request.query_params.get("orderBy")
        location = self.request.query_params.get("location")

        if company:
            queryset = queryset.filter(company=company)
        if remote == "true":
            queryset = queryset.filter(remote=True)
        if remote == "false":
            queryset = queryset.filter(remote=False)
        if order_by == "title":
            queryset = queryset.order_by("title")
        if order_by == "company":
            queryset = queryset.order_by("company__name")
        if order_by == "date":
            queryset = queryset.order_by("-date")
        if location:
            queryset = queryset.filter(location=location)

        return queryset


class LocationsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        queryset = (
            Job.objects.distinct("location")
            .filter(active=True)
            .exclude(location="")
            .values_list("location", flat=True)
        )

        return Response({"locations": queryset})
