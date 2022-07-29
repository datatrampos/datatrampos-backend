from jobs.models import Job


class RegisterJobs():
    
    @staticmethod
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
