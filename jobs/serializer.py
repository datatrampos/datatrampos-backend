from rest_framework import serializers

from companies.serializer import CompanySerializer
from jobs.models import Job


class JobSerializer(serializers.ModelSerializer):

    company = CompanySerializer()

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "company",
            "remote",
            "date",
            "location",
            "seniority",
            "url",
        ]
