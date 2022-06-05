from django.contrib import admin
from django.urls import path, include
from jobs.views import JobsViewSet
from companies.views import CompaniesViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'jobs', JobsViewSet)
router.register(r'companies', CompaniesViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
