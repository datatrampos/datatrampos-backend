from rest_framework import serializers
from companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name',
                  'linkedin',
                  'website',
                  'glassdoor',
                  'logo']
