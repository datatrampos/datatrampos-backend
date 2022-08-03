from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

from jobs.management.commands._private import fix_workplace_name, update_get_company, save_job, remote_show


class Greenhouse():
    help = "collect jobs"

    def get_company_info(self, company_url, company_name):

        company_page = urlopen(company_url)

        soup = BeautifulSoup(company_page, "html.parser")

        try:
            logo_div = soup.find("div", {"id": "logo"})
            logo = logo_div.find("img")["src"]
            logo_bin = urlopen(logo).read()
        except:
            logo_bin = None

        website = None

        glassdoor = None

        linkedin = None

        company = update_get_company(company_url=company_url, company_name=company_name,
                                     website=website, glassdoor=glassdoor, linkedin=linkedin, logo_bin=logo_bin)

        return company

    def get_job(self, company, terms, exceptions):
        job_urls_list = []

        print(company["website"])

        website = urlopen(company["website"])

        bs = BeautifulSoup(website, "html.parser")
        bs = bs.find('div', {'id': 'main'})
        sections = bs.find_all('section', {'class': 'level-0'})

        try:
            c = self.get_company_info(
                company_url=company["website"],
                company_name=company["company_name"],
            )
        except Exception as e:
            print(e)

        for section in sections:
            positions = section.find_all('div')
            for job in positions:
                role_find = job.find('a', href=True)
                role = role_find.text
                roleSplited = re.sub('[,.;@#?!/\|&$)(-]+\|*', ' ', role).lower().split()
                for term in terms:
                    if all(elem in roleSplited for elem in term.lower().split()):
                        if not any(e in role for e in exceptions):
                            workplace = job.find('span', {'class': 'location'}).text
                            remote_status = remote_show(role) or remote_show(workplace)
                            url = 'https://boards.greenhouse.io' + role_find['href']

                            workplace_parsed = fix_workplace_name(
                                workplace) if workplace != '' else ''
                            try:
                                save_job(
                                    title=role, url=url, remote=remote_status, location=workplace_parsed, company=c)

                            except Exception as e:
                                print(e)

                            job_urls_list.append(url)

        return job_urls_list
