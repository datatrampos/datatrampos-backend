import json
from urllib.error import HTTPError
from django.core.management.base import BaseCommand
from django.db.models import Q
from jobs.management.commands.scrape_lever import Lever

from jobs.models import Job
from companies.models import Company
from jobs.management.commands.scrape_gupy import Gupy
from jobs.management.commands.scrape_greenhouse import Greenhouse

TERMS = [
    "BI",
    "Business Intelligence",
    "Python",
    "Data",
    "Dados",
    "Analysis",
    "Data Analyst",
    "Analytics",
    "Machine Learning",
    "ML",
    "Intelligence",
    "Fraud",
    "Artificial",
    "AI",
]

EXCEPTIONS = []

LIST_OF_ACTIVE_JOB_URLS = []

with open(r"./jobs/management/commands/companiesv2.json") as file:
    companies_list = json.load(file)


class Command(BaseCommand):

    def handle(self, *args, **options):
        gupy_scraper = Gupy()
        greenhouse_scraper = Greenhouse()
        lever_scraper = Lever()

        for company in companies_list['jobs_sources']:
            try:
                if company['source'] == 'gupy':
                    active_jobs_gupy = gupy_scraper.get_job(
                        company=company, terms=TERMS, exceptions=EXCEPTIONS)
                    LIST_OF_ACTIVE_JOB_URLS.extend(active_jobs_gupy)

                elif company['source'] == 'greenhouse':
                    active_jobs_greenhouse = greenhouse_scraper.get_job(company=company, terms=TERMS,
                                                                        exceptions=EXCEPTIONS)
                    LIST_OF_ACTIVE_JOB_URLS.extend(active_jobs_greenhouse)

                elif company['source'] == 'lever':
                    active_jobs_lever = lever_scraper.get_job(company=company, terms=TERMS,
                                                              exceptions=EXCEPTIONS)
                    LIST_OF_ACTIVE_JOB_URLS.extend(active_jobs_lever)
                else:
                    continue
            except Exception as e:
                print(e)
                print("\033[93m" + company['website'] +
                      " -> source is broken" + "\033[0m")
                continue

        Job.objects.filter(~Q(url__in=LIST_OF_ACTIVE_JOB_URLS)
                           ).update(active=False)
