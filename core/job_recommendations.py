from urllib.parse import quote_plus


# =========================================
# JOB SEARCH LINKS
# =========================================

def get_job_links(target_job):

    encoded_job = quote_plus(target_job)

    links = {

        "LinkedIn": (
            f"https://www.linkedin.com/jobs/search/"
            f"?keywords={encoded_job}"
        ),

        "Indeed": (
            f"https://www.indeed.com/jobs"
            f"?q={encoded_job}"
        ),

        "Wellfound": (
            f"https://wellfound.com/jobs"
            f"?query={encoded_job}"
        ),

        "Internshala": (
            f"https://internshala.com/jobs/"
            f"keywords-{encoded_job.replace('+', '-')}/"
        ),

        "Naukri": (
            f"https://www.naukri.com/"
            f"{encoded_job.replace('+', '-')}-jobs"
        )
    }

    return links