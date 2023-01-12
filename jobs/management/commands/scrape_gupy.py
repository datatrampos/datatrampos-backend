import requests
from bs4 import BeautifulSoup
import re
import json

from jobs.management.commands._private import fix_workplace_name, update_get_company, save_job


class Gupy():
    help = "collect jobs"

    def get_company_info(self, data, company_url, company_name):

        logo_src = data.get("urlLogo")
        logo_bin = requests.get(logo_src).content

        urls = [section for section in data.get(
            'sections') if section['type'] == "social_links_section"]

        website = urls[0].get('urlSite') if len(
            urls) > 0 and urls[0].get('urlSite') else None

        linkedin = urls[0].get('urlLinkedin') if len(
            urls) > 0 and urls[0].get('urlLinkedin') else None

        glassdoor = urls[0].get('urlGlassdoor') if len(
            urls) > 0 and urls[0].get('urlGlassdoor') else None

        company = update_get_company(company_url=company_url, company_name=company_name,
                                     website=website, glassdoor=glassdoor, linkedin=linkedin, logo_bin=logo_bin)
        return company

    def get_job(self, company, terms, exceptions):

        job_urls_list = []

        print(company["website"])

        req = requests.get(company["website"])

        bs = BeautifulSoup(req.content, "html.parser")

        script = bs.find("script", {"id": "__NEXT_DATA__"}).text

        page_data = json.loads(script)

        data = page_data.get('props').get('pageProps').get('careerPage')
        

        try:
            c = self.get_company_info(
                data=page_data.get('props').get('pageProps').get('careerPage'),
                company_url=company["website"],
                company_name=company["company_name"],
            )
        except Exception as e:
            print(e)
        
        job_list = page_data.get('props').get('pageProps').get('jobs')

        section_list = bs.find("ul", {"aria-label": "Lista de Vagas"})
        urls_list = [li.find("a", href=True)["href"] for li in section_list]

        for job, url in zip(job_list, urls_list):
            role = job.get("title")
            roleSplited = re.sub('[,.;@#?!/\|&$)(-]+\|*', ' ', role).lower().split()
            remote_status = job.get("workplace").get("remoteWorking")
            workplace = job.get("workplace").get("address").get("city")

            for term in terms:
                if all(elem in roleSplited for elem in term.lower().split()):
                    if not any(e in role for e in exceptions):
                        workplace_parsed = fix_workplace_name(
                            workplace) if workplace != '' else ''
                        try:
                            save_job(
                                title=role, url=company["website"] + url, remote=remote_status, location=workplace_parsed, company=c)

                        except Exception as e:
                            print(e)

                        job_urls_list.append(company["website"] + url)

        return job_urls_list
