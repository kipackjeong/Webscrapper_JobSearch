import requests
from bs4 import BeautifulSoup
from scrappers.job import Job

class StackoverflowScrapper(object):
    def __init__(self, word) -> None:
        self.url = f'https://stackoverflow.com/jobs?q={word}&sort=p'

    def get_max_page(self):
        print("Extracting last page from Stackoverflow....")
        page_nums = []
        request = requests.get(self.url)
        html = BeautifulSoup(request.text, 'html.parser')
        pagination = html.find('div',{'class':'s-pagination'})
        pages = pagination.find_all('a')
        for page in pages:
            page_nums.append(page.find('span').string)
        max_page = int(page_nums[-2])
        print(f'Stackoverflow max page: {max_page}')
        return int(page_nums[-2])
        
    def extract_jobs(self):
        def extract_title(job_info):
            return job_info.find('h2',{'class':'mb4'}).find('a')['title']    
        def extract_company(job_info):
            return job_info.find('h3', {'class':'mb4'}).find('span').get_text(strip=True)
        def extract_location(job_info):
            return job_info.find('h3', {'class':'mb4'}).find('span',class_='fc-black-500').get_text(strip=True)
        def extract_date(job_info):
            return job_info.find('ul', class_='mt4').find('span').get_text(strip=True)
        def extract_applylink(job_number):
            return 'https://stackoverflow.com/jobs/' + job_number

        
        print(f"extracting jobs from Stackoverflow...")
        jobs = []
        max_page = 2
        for n in range(1,max_page + 1):
            if n == 1:
                request = requests.get(self.url)
            else:
                request = requests.get(self.url + f'pg={n}')
            html = BeautifulSoup(request.text, 'html.parser')
            div_jobs = html.find_all('div', {'class':'-job'})
            for div_job in div_jobs:
                job_info = div_job.find('div', {'class':'fl1'})
                title = extract_title(job_info)
                company = extract_company(job_info)
                location = extract_location(job_info)
                applylink = extract_applylink(div_job['data-jobid'])
                date = extract_date(job_info)
                job = Job(title, company,location, 'NA', 'NA', date, applylink)
                jobs.append(job)
        print(f'Stackoverflow job extracting finished')
        return jobs

        
    