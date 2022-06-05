from django.contrib import admin
from companies.models import Company

class Companies(admin.ModelAdmin):
    list_display = ('url',
                    'name',
                    'linkedin',
                    'website',
                    'glassdoor',
                    'logo')

    list_display_links = ('name')
    search_fields = ('name',)


admin.site.register(Company)
