import requests
from bs4 import BeautifulSoup
import re

from jobs.management.commands._private import fix_workplace_name, update_get_company, save_job, remote_show


class Lever():
    help = "collect lever jobs"

    def get_company_info(self, company_url, company_name):

        page = requests.get(company_url)

        soup = BeautifulSoup(page.content,  "html.parser")

        logo_container = soup.find("a", {"class": "main-header-logo"})
        logo_src = logo_container.find("img")["src"]
        logo_bin = requests.get(logo_src).content

        footer_container = soup.find("div", {"class": "main-footer-text"})
        website = footer_container.find("p").find("a")["href"]

        company = update_get_company(company_url=company_url, company_name=company_name,
                                     website=website, glassdoor=None, linkedin=None, logo_bin=logo_bin)

        return company

    def get_job(self, company, terms, exceptions):

        job_urls_list = []
        
        print(company["website"])

        req = requests.get(company["website"])

        bs = BeautifulSoup(req.content, "html.parser")

        try:
            c = self.get_company_info(
                company_url=company["website"],
                company_name=company["company_name"],
            )
        except Exception as e:
            print(e)

        jobs_wrapper = bs.find("div", {"class": "postings-wrapper"})
        jobs = jobs_wrapper.find_all("div", {"class": "posting"})

        for job in jobs:

            link = job.find('a', {"class": "posting-title"}, href=True)["href"]
            role = job.find('h5', {'data-qa': 'posting-name'}).text
            roleSplited = re.sub('[,.;@#?!/\|&$)(-]+\|*', ' ', role).lower().split()

            for term in terms:
                if all(elem in roleSplited for elem in term.lower().split()):
                    if not any(e in role for e in exceptions):
                        workplace = job.find('span', {'class': 'location'}).text
                        workplace_status = job.find('span', {'class': 'workplaceTypes'})
                        remote_status = remote_show(role) or remote_show(
                            workplace) or remote_show(workplace_status.text if workplace_status is not None else '')
                        url = link

                        workplace_parsed = fix_workplace_name(
                            workplace) if workplace != '' else ''
                        try:
                            save_job(
                                title=role, url=url, remote=remote_status, location=workplace_parsed, company=c)

                        except Exception as e:
                            print(e)

                        job_urls_list.append(url)

        return job_urls_list
