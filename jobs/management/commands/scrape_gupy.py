from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

from jobs.management.commands._private import fix_workplace_name, update_get_company, save_job


class Gupy():
    help = "collect jobs"

    def get_company_info(self, soup, company_url, company_name):

        logo = soup.find("div", {"class", "header__logo"}).find("img")["src"]
        logo_bin = urlopen(logo).read()

        try:
            social_medias = soup.find("ul", {"class", "description__social"})
            urls = [
                li.find("a", href=True)["href"] for li in social_medias.find_all("li")
            ]
        except Exception:
            urls = [None, " ", " "]

        website = urls[0]
        linkedin = urls[1] if "linkedin" in urls[1] else None
        glassdoor = urls[-1] if "glassdoor" in urls[-1] else None

        company = update_get_company(company_url=company_url, company_name=company_name,
                               website=website, glassdoor=glassdoor, linkedin=linkedin, logo_bin=logo_bin)
        return company

    def get_job(self, company, terms, exceptions):

        job_urls_list = []

        print(company["website"])

        website = urlopen(company["website"])

        bs = BeautifulSoup(website, "html.parser")

        try:
            c = self.get_company_info(
                soup=bs,
                company_url=company["website"],
                company_name=company["company_name"],
            )
        except Exception as e:
            print(e)

        job_list = bs.find("div", {"class": "job-list jobs-to-filter"})
        table = job_list.find("table")
        rows = table.find_all("tr")

        for row in rows:

            data = row.find("h4")
            role = data.find("span").text
            roleSplited = re.sub('[,.;@#?!/\|&$)(-]+\|*', ' ', role).lower().split()

            for term in terms:
                if all(elem in roleSplited for elem in term.lower().split()):
                    if not any(e in role for e in exceptions):
                        a = row.find("a", href=True)
                        workplace = row["data-workplace"]
                        workplace_parsed = fix_workplace_name(
                            workplace) if workplace != '' else ''
                        remote = row["data-remote"]

                        remote_status = remote.lower() in [
                            "true", "1", "t", "y", "yes", "True"]
                        try:
                            save_job(
                                title=role, url=company["website"] + a["href"], remote=remote_status, location=workplace_parsed, company=c)

                        except Exception as e:
                            print(e)

                        job_urls_list.append(company["website"] + a["href"])

        return job_urls_list
