from django.contrib import admin
from jobs.models import Job


class Jobs(admin.ModelAdmin):
    list_display = (
        "title",
        "company_name",
        "remote",
        "date",
        "location",
        "seniority",
        "url",
    )

    list_display_links = "title"
    search_fields = ("title",)


admin.site.register(Job)
