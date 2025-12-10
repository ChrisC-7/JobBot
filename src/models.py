# src/models.py

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class JobPosting:
    id: str  # The job id in the linkedin 
    title: str
    company: str
    location: str
    url: str
    description: str
    posted_at: Optional[datetime] = None
    source: str = 'linkedin'
    seniority: Optional[str] = None        # e.g. "Intern", "Entry level"
    employment_type: Optional[str] = None  # e.g. "Full-time", "Internship

@dataclass
class ScoredJob:
    '''
    The job after scored by LLM
    '''
    job: JobPosting
    skill_score: float
    experience_score: float
    education_score: float
    bonus_score: float
    total_score: float

    apply_recommendation: str             # "Strong Yes" / "Yes" / "Maybe" / "No"
    key_reasons: List[str]                # 1-3 key reasons
    explanation: str                      # some summary explaination

    # for future auto apply
    auto_apply_supported: bool = False