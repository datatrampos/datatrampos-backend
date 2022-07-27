from django.contrib import admin
from django.urls import path, include
from jobs.views import JobsViewSet, LocationsView
from companies.views import CompaniesViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"jobs", JobsViewSet, basename="Job")
router.register(r"companies", CompaniesViewSet, basename="Company")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("locations", LocationsView.as_view()),
]
