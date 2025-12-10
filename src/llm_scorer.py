# src/llm_scorer.py

# export GEMINI_API_KEY = "YOUR_API_KEY"
PROMPT_TEMPLATE = """
You are an assistant that evaluates how well a candidate's CV matches a specific job posting.

You will receive:
1. The candidate's CV.
2. The job posting information (title, company, location, and job description).

You must score the match on FOUR dimensions. Each score is from 0 to 100:

1. skill_score:
   - How well the candidate's technical skills, tools, and technologies match
     the core skills required by the job.
   - Consider programming languages, frameworks, ML/AI tools, data tools, etc.

2. experience_score:
   - How well the candidate's projects, internships, work experience, or
     research experience match the responsibilities and domain of the job.
   - Consider similarity in problem types, domains, and scale.

3. education_score:
   - How well the candidate's education and research background (degree, major,
     relevant coursework, research, publications) match the job's expectations.

4. bonus_score:
   - Extra factors that make the candidate stand out: open-source contributions,
     competitions, side projects, leadership, community work, etc.

Then set:
- apply_recommendation: one of "Strong Yes", "Yes", "Maybe", "No".
- key_reasons: a short list (1-3 strings) explaining the main reasons for your evaluation.
- explanation: a short paragraph summarizing your evaluation.

IMPORTANT:
- Each of skill_score, experience_score, education_score, bonus_score MUST be a number between 0 and 100.
- You MUST return ONLY a valid JSON object with ALL of the following keys:
  "skill_score", "experience_score", "education_score", "bonus_score", 
  "apply_recommendation", "key_reasons", "explanation".
- Do NOT include any text before or after the JSON. No backticks, no comments, no prose.

---
CANDIDATE_CV:
{cv_text}

---
JOB_POSTING:
Title: {title}
Company: {company}
Location: {location}

Description:
{description}
The role might be Software Engineer, AI/ML/Research, or Data-focused.
When scoring, you should infer the role type from the job description
and adjust your interpretation of "skills" and "experience" accordingly.
For example:
- For Software Engineer roles, focus on coding, systems, and engineering skills.
- For AI/ML roles, focus on ML/AI frameworks, modeling, and research experience.
- For Data roles, focus on statistics, SQL, analytics, and business understanding.
"""

from src.models import JobPosting, ScoredJob
from src.scoring import calculate_total_score_from_scores
from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class modelConfig:
    model_name = "gemini-3-pro-preview"

class LLMOutput(BaseModel):
    skill_score: float = Field(description="Score 0-100 based on technical skills match")
    experience_score: float = Field(description="Score 0-100 based on work history match")
    education_score: float = Field(description="Score 0-100 based on degree and research")
    bonus_score: float = Field(description="Score 0-100 based on extra achievements")
    
    apply_recommendation: str = Field(description="Strong Yes, Yes, Maybe, or No")
    key_reasons: List[str] = Field(description="List of 1-3 key reasons for the score")
    explanation: str = Field(description="Brief summary of the evaluation")

class JobLLMScorer:
    def __init__(self, cv_text:str,  client: Optional[Any] = None):
        self.cv = cv_text 
        self.client = client or self._default_client()
        
    def _default_client(self):
        from google import genai
        return genai.Client()

    def score_job(self, job:JobPosting) -> ScoredJob:
        prompt = self._generate_prompt(job)
        try:
            data = self._call_LLM(prompt)
        except ValueError as e:
            print(f"[LLM scoring failed for job {job.title}]: {e}")
            raise

        scored_job = self._build_scored_job(job, data)
        return scored_job

    def _generate_prompt(self, job:JobPosting) -> str:
        return PROMPT_TEMPLATE.format(
            cv_text = self.cv,
            title = job.title, 
            company = job.company,
            location = job.location,
            description = job.description)
    
    def _call_LLM(self, prompt:str) -> LLMOutput:
        response = self.client.models.generate_content(
            model = modelConfig.model_name,
            contents = prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': LLMOutput,
            }
        )
        eval_result = response.parsed
        if not eval_result:
            raise ValueError(f"Failed to parse result")
        
        return eval_result



    def _build_scored_job(self, job: JobPosting, data:LLMOutput) -> ScoredJob:
        total_score = calculate_total_score_from_scores(
            data.skill_score,
            data.experience_score,
            data.education_score,
            data.bonus_score
        )
        return ScoredJob(
            job = job,
            skill_score = data.skill_score,
            experience_score = data.experience_score,
            education_score = data.education_score,
            bonus_score = data.bonus_score,
            total_score = total_score,
            apply_recommendation = data.apply_recommendation,
            key_reasons = data.key_reasons,
            explanation = data.explanation,
            auto_apply_supported = False
        )