# src/scorer.py
'''
The Job Scorer
'''
from src.models import JobPosting, ScoredJob


class JobScorer:
    def __init__(self, cv_text:str):
        pass

    def score_job(self, job:JobPosting) -> ScoredJob:
        