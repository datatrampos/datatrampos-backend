from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from companies.models import Company
from companies.serializer import CompanySerializer


class CompaniesViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (AllowAny,)
