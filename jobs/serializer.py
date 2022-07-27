from attr import field
from rest_framework import serializers
from jobs.models import Job
from companies.serializer import CompanySerializer


class JobSerializer(serializers.ModelSerializer):

    company = CompanySerializer()

    class Meta:
        model = Job
        fields = ['location',
                  'url',
                  'title',
                  'company',
                  'remote',
                  'date',
                  'seniority']


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = ['location']
