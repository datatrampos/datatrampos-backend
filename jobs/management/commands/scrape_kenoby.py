from atexit import register
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

from jobs.management.commands._private import RegisterJobs
from companies.models import Company


class Kenoby():
    help = "collect jobs"

    def get_company_info(self, company_url, company_name):

        company_page = urlopen(company_url)

        soup = BeautifulSoup(company_page, "html.parser")

        logo = soup.find("link", rel="shortcut icon")['href']
        logo_bin = urlopen(logo).read()

        try:
            website = soup.find('a', {"title", "Site"})['href']
        except:
            website = None

        try:
            glassdoor = soup.find('a', {"title", "Glassdoor"})['href']
        except:
            glassdoor = None

        try:
            linkedin = soup.find('a', {"title", "Linkedin"})['href']
        except:
            linkedin = None

        company, _ = Company.objects.get_or_create(
            url=company_url,
            defaults={
                "name": company_name,
                "website": website,
                "linkedin": linkedin,
                "glassdoor": glassdoor,
                "logo": logo_bin,
            },
        )
        return company

    def get_job(self, company, terms, exceptions):
        job_urls_list = []
        auxiliar_remote_terms = ["remoto", "remote"]

        print(company["website"])

        website = urlopen(company["website"]+'/position')

        bs = BeautifulSoup(website, "html.parser")
        bs = bs.find('div', {'id': 'content'})
        list_of_segments = bs.find_all('div', {'class': 'segment'})

        try:
            c = self.get_company_info(
                company_url=company["website"],
                company_name=company["company_name"],
            )
        except Exception as e:
            print(e)

        for segment in list_of_segments:
            position = segment.find('div', {'class': 'positions'})
            for job in position.find_all('a'):
                role = job['data-title']
                roleSplited = re.sub(r"[,.;@#?!/&$)(-]+\|*",
                                     " ", role).lower().split()
                for term in terms:
                    if all(elem in roleSplited for elem in term.lower().split()):
                        if not any(e in role for e in exceptions):
                            workplace = job['data-city']
                            state = job['data-state']
                            remote_status = True if any(appear in auxiliar_remote_terms for appear in roleSplited +
                                                        workplace.lower().split()+state.lower().split()) else False

                            try:
                                RegisterJobs.save_job(
                                    title=role, url=job['href'], remote=remote_status, location=workplace, company=c)

                            except Exception as e:
                                print(e)

                            job_urls_list.append(job['href'])

        return job_urls_list
