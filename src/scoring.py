# src/scoring.py

'''
How to score the Total score based on the four basic scores
Total score = 
Skill Match: 0.45
Experience Match: 0.35
Education & Research: 0.15
Bonus / Culture Fit: 0.05
'''
skill_weight = 0.45
experience_weight = 0.35
education_weight = 0.15
bounus_weight = 0.05

from src.models import ScoredJob
def calculate_total_score_from_scores(  skill_score: float,
                            experience_score: float,
                            education_score: float, 
                            bonus_score: float):
    return skill_weight * skill_score + experience_weight * experience_score + education_weight * education_score + bounus_weight * bonus_score

def calculate_total_score_for_job( job: ScoredJob):
    job.total_score = calculate_total_score_from_scores(job.skill_score, job.experience_score, job.education_score, job.bonus_score)
    return 