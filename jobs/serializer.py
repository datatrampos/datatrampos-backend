from rest_framework import serializers
from jobs.models import Job
from companies.serializer import CompanySerializer


class JobSerializer(serializers.ModelSerializer):

    company = CompanySerializer()

    class Meta:
        model = Job
        fields = ['id', 'title',
                  'company',
                  'remote',
                  'date',
                  'location',
                  'seniority', 'url']
