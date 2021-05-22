from time import sleep
from celery import shared_task
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from .models import Job
import json
from django.conf import settings

with open(f'{settings.BASE_DIR}/core/jobs.json') as file:
    companies_list = json.load(file)

gupy = companies_list["jobs_sources"]["gupy"]
list_of_interests = ["BI", "Business Intelligence", "Python", "Data", "Dados", "Analysis", "Data Analyst", "Analytics","Machine Learning"]

@shared_task
def fetch_data(companies_list, list_of_interests):
    for item in companies_list:
        site = urlopen(item['website'])
        bs = BeautifulSoup(site, 'html.parser')
        bs = bs.find("div", {'class': 'job-list'})
        table = bs.find("table")
        rows = table.find_all('tr')
        jobs = []
        for row in rows:
            location = row['data-workplace']
            isRemote = row['data-remote']
            data = row.find("h4")
            a = row.find("a", href=True)
            cargo = data.find("span").text
            for i in list_of_interests:
                if i in cargo:
                    company = item['company_name']
                    job_title = cargo
                    url = item['website'] + a['href']
                    remote = isRemote
                    workplace = location

                    print({'company': company, 'job_title': job_title,
                           'url': url, 'remote': remote, 'workplace': workplace})

                    Job.objects.create(
                        company_name=company,
                        job_title=job_title,
                        url=url,
                        remote=remote,
                        workplace=workplace
                    )

                    sleep(5)

fetch_data(gupy, list_of_interests)