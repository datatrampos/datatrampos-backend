import re

from jobs.models import Job
from companies.models import Company


def save_job(title, url,  remote, location, company):

    Job.objects.update_or_create(
        url=url,
        defaults={
            "title": title,
            "remote": remote,
            "location": location,
            "company": company,
            "active": True,
        },
    )
    print("%s added" % (title,))


def update_get_company(company_url, company_name, website, linkedin, glassdoor, logo_bin):
    Company.objects.update_or_create(
        url=company_url,
        defaults={
            "name": company_name,
            "website": website,
            "linkedin": linkedin,
            "glassdoor": glassdoor,
            "logo": logo_bin,
        },
    )

    company = Company.objects.get(url=company_url)

    return company


def fix_workplace_name(text):
    SP_MAP = ['são paulo', 'sao paulo']
    BR_MAP = ['brasil', 'brazil']

    remote_hybrid_map_words = ['Remoto', 'remote', 'Remote', 'Híbrido',
                               'hibrido', 'Hibrido', 'remoto', 'REMOTO', 'REMOTE']
    text_splitted = re.sub('[,.;@#?!/\|&$)(-]+\|*', ' ', text).split()
    text_formatted = [
        item for item in text_splitted if item not in remote_hybrid_map_words]

    for sp in SP_MAP:
        if sp in text.lower():
            return "São Paulo"

    if "curitiba" in text.lower():
        return "Curitiba"

    if "rio de janeiro" in text.lower():
        return "Rio de Janeiro"

    if text.lower() in BR_MAP:
        return "Brasil"

    return (' ').join(text_formatted)


def remote_show(text):
    remote_map_words = ['remoto', 'remote']
    text_splitted = re.sub('[,.;@#?!/\|&$)(-]+\|*', ' ', text).lower().split()
    return any(item in remote_map_words for item in text_splitted)