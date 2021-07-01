import csv
from job import Job
from typing import List

def save_to_csv(jobs:List[Job]):
    print('saving jobs to csv...')
    with open('jobs.csv', 'w', encoding ='utf-8', newline='') as csvfile:
        jobwriter = csv.writer(csvfile)
        jobwriter.writerow(['Title','Company','Location','Date','Salary','Apply'])
        for job in jobs:
            jobwriter.writerow([str(job.title),str(job.company),str(job.location),str(job.date),str(job.salary),str(job.apply_url)])
    print('finished')


    