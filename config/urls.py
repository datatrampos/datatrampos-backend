from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from companies.views import CompaniesViewSet
from jobs.views import JobsViewSet

router = routers.DefaultRouter()
router.register(r"jobs", JobsViewSet, basename="Job")
router.register(r"companies", CompaniesViewSet, basename="Company")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]
