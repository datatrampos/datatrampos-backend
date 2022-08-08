from rest_framework.pagination import PageNumberPagination


class CustomJobsResultsSetPagination(PageNumberPagination):
    page_size = 16
