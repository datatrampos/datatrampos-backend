from curses import ALL_MOUSE_EVENTS
from ssl import ALERT_DESCRIPTION_UNSUPPORTED_CERTIFICATE
from rest_framework import viewsets
from companies.models import Company
from companies.serializer import CompanySerializer


class CompaniesViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
