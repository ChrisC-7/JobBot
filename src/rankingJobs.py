# src/rankingJobs.py
'''
The min score that used to fliter the jobs: 60
The max jobs that  used to send to me: 30
if there are less than 30 jobs whose score higher than 60, just send me the jobs
'''
from src.models import ScoredJob
from typing import List
min_total_score = 60
max_jobs_per_day = 30

def get_total_score(job: ScoredJob):
    return job.total_score


def rankedJobs(jobs:List[ScoredJob]):
    ranked_jobs = sorted(jobs, key=get_total_score, reverse=True)
    filtered_jobs = list(filter(lambda x: x.total_score >= min_total_score, ranked_jobs))
    if len(filtered_jobs) > max_jobs_per_day :
        return filtered_jobs[:max_jobs_per_day]
    return filtered_jobs