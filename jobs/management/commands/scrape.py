from django.core.management.base import BaseCommand
from django.db.models import Q
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re

from jobs.models import Job
from companies.models import Company

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

with open(r"./jobs/management/commands/companies.json") as file:
    companies_list = json.load(file)

GUPY_URLs = companies_list["jobs_sources"]["gupy"]


class Command(BaseCommand):
    help = "collect jobs"

    def getCompanyInfo(self, soup, company_url, company_name):

        logo = soup.find("div", {"class", "header__logo"}).find("img")["src"]
        logo_bin = urlopen(logo).read()

        try:
            social_medias = soup.find("ul", {"class", "description__social"})
            urls = [
                li.find("a", href=True)["href"] for li in social_medias.find_all("li")
            ]
        except Exception:
            urls = [None, " ", " "]

        company, _ = Company.objects.get_or_create(
            url=company_url,
            defaults={
                "name": company_name,
                "website": urls[0],
                "linkedin": urls[1] if "linkedin" in urls[1] else None,
                "glassdoor": urls[-1] if "glassdoor" in urls[-1] else None,
                "logo": logo_bin,
            },
        )
        return company

    def handle(self, *args, **options):

        list_of_active_job_urls = []

        for company in GUPY_URLs:
            print(company["website"])

            try:
                website = urlopen(company["website"])
            except Exception as e:
                print(e)
                continue

            bs = BeautifulSoup(website, "html.parser")

            try:
                c = self.getCompanyInfo(
                    soup=bs,
                    company_url=company["website"],
                    company_name=company["company_name"],
                )
            except Exception as e:
                print(e)

            job_list = bs.find("div", {"class": "job-list"})
            table = job_list.find("table")
            rows = table.find_all("tr")

            for row in rows:

                a = row.find("a", href=True)
                workplace = row["data-workplace"]
                remote = row["data-remote"]
                data = row.find("h4")
                role = data.find("span").text
                roleSplited = re.sub(r"[,.;@#?!/&$)(-]+\|*", " ", role).lower().split()

                for term in TERMS:
                    if all(elem in roleSplited for elem in term.lower().split()):
                        if not any(e in role for e in EXCEPTIONS):
                            try:
                                Job.objects.update_or_create(
                                    url=company["website"] + a["href"],
                                    defaults={
                                        "title": role,
                                        "remote": remote.lower()
                                        in ["true", "1", "t", "y", "yes", "True"],
                                        "location": workplace,
                                        "company": c,
                                        "active": True,
                                    },
                                )
                                print("%s added" % (role,))

                                list_of_active_job_urls.append(
                                    company["website"] + a["href"]
                                )
                            except Exception as e:
                                print(e)

        Job.objects.filter(~Q(url__in=list_of_active_job_urls)).update(active=False)

        self.stdout.write("job complete")
