from rest_framework import viewsets
from companies.models import Company
from companies.serializer import CompanySerializer


class CompaniesViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    http_method_names = ['get']
