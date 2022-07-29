from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

from jobs.management.commands._private import RegisterJobs
from companies.models import Company


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

            for term in terms:
                if all(elem in roleSplited for elem in term.lower().split()):
                    if not any(e in role for e in exceptions):

                        remote_status = remote.lower() in ["true", "1", "t", "y", "yes", "True"]
                        try:
                            RegisterJobs.save_job(
                                title=role, url=company["website"] + a["href"], remote=remote_status, location=workplace, company=c)

                        except Exception as e:
                            print(e)

                        job_urls_list.append(company["website"] + a["href"])
                        
        return job_urls_list
