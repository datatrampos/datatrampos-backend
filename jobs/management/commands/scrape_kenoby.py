from atexit import register
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

from jobs.management.commands._private import update_get_company, save_job, fix_workplace_name, remote_show, is_kenoby_icon
from companies.models import Company


class Kenoby():
    help = "collect jobs"

    def get_company_info(self, company_url, company_name):

        company_page = urlopen(company_url)

        soup = BeautifulSoup(company_page, "html.parser")

        logo = soup.find("link", rel="shortcut icon")['href']
        if is_kenoby_icon(logo) == False:
            logo_bin = urlopen(logo).read()
        else:
            logo_bin = None

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

        company = update_get_company(company_url=company_url, company_name=company_name,
                                     website=website, glassdoor=glassdoor, linkedin=linkedin, logo_bin=logo_bin)

        return company

    def get_job(self, company, terms, exceptions):
        job_urls_list = []

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
                roleSplited = re.sub('[,.;@#?!/\|&$)(-]+\|*', ' ', role).lower().split()
                for term in terms:
                    if all(elem in roleSplited for elem in term.lower().split()):
                        if not any(e in role for e in exceptions):
                            workplace = job['data-city']
                            state = job['data-state']
                            remote_status = remote_show(role) or remote_show(
                                workplace) or remote_show(state)

                            workplace_parsed = fix_workplace_name(
                                workplace) if workplace != '' else ''
                            try:
                                save_job(
                                    title=role, url=job['href'], remote=remote_status, location=workplace_parsed, company=c)

                            except Exception as e:
                                print(e)

                            job_urls_list.append(job['href'])

        return job_urls_list
