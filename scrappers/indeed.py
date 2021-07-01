import requests
from bs4 import BeautifulSoup
from scrappers.job import Job


class IndeedScrapper(object):
    def __init__(self, word):
        self.url = f"https://www.indeed.com/jobs?q={word}&fromage=1&sort=date&limit=50"
        self.max_page = 10

    def get_max_page(self):
        pages = set()

        def helper(last):
            Url = self.url + f"&start={last * 50}"
            request = requests.get(Url)
            html = BeautifulSoup(request.text, 'html.parser')
            pagination = html.find('div', {'class': 'pagination'})
            page_links = pagination.find_all('span')
            self.max_page = last
            for page_link in page_links:
                if page_link.string:
                    page_num = int(page_link.string)
                    self.max_page = max(page_num, last)
                    pages.add(int(page_link.string))
            if self.max_page == last:
                return self.max_page
            return helper(self.max_page)

        print("Extracting last page from Indeed....")
        self.max_page = helper(0)
        print(f"Indeed max page: {self.max_page}")
        return self.max_page

    # return list of Job objects
    def extract_jobs(self):
        def extract_title(div_job):
            job_title = div_job.find('h2', {
                'class': 'jobTitle'
            }).find('span', {'class': not 'label'})['title'].strip()

            return job_title

        def extract_company(div_job):
            company_name = ''
            span_tag = div_job.find('span', {'class': 'companyName'})
            if span_tag.a:
                company_name = span_tag.find('a').string.strip()
            else:
                company_name = span_tag.string
            return company_name

        def extract_location(div_job):
            location = div_job.find('div', {'class': 'companyLocation'})
            return location.string

        def extract_salary(div_job):
            sal_snippet = div_job.find('span', {'class': 'salary-snippet'})
            sal_snippet = sal_snippet.string.strip() if sal_snippet else 'NA'

            return sal_snippet

        def extract_summary(div_job):
            descriptions = div_job.find('div', {
                'class': 'job-snippet'
            }).find_all('li')
            summary = ''
            for i, description in enumerate(descriptions):
                if description.string:
                    if i == len(descriptions) - 1:
                        summary += '-' + description.string
                    else:
                        summary += '-' + description.string + '\n'
            return summary

        def extract_date(div_job):
            return div_job.find('span', {'class': 'date'}).string.strip()

        def extract_url(div_job):
            return 'https://www.indeed.com' + div_job['href']

        print(f"extracting jobs from Indeed...")
        urls = []
        jobs = []
        for n in range(self.max_page):
            urls.append(self.url + f'start={n*50}')
        for url in urls:
            request = requests.get(url)
            html = BeautifulSoup(request.text, 'html.parser')
            div_jobs = html.find_all('a', {'class': 'result'})

            for div_job in div_jobs:
                if div_job:
                    # job = Job(extract_title(div_job), extract_company(div_job),
                    #           extract_location(div_job), extract_salary(div_job),
                    #           extract_summary(div_job), extract_date(div_job),
                    #           extract_url(div_job))
                    # jobs.append(job)
                    job = Job(
                    extract_title(div_job),
                    extract_company(div_job),
                    extract_location(div_job),
                    extract_salary(div_job),
                    extract_summary(div_job),
                    extract_date(div_job),
                    extract_url(div_job))
                    jobs.append(job)
                    
        print(f'Indeed job extracting finished')
        return jobs
