# test/test_llm_scorer.py

import unittest
from datetime import datetime

from src.llm_scorer import JobLLMScorer, LLMOutput
from src.models import JobPosting, ScoredJob
from src.scoring import calculate_total_score_from_scores


# ---------- Fake for Gemini Client -------------
class FakeResponse:
    def __init__(self, parsed):
        self.parsed = parsed

class FakeModels:
    def __init__(self, parsed_output):
        self._parsed_output = parsed_output
    
    def generate_content(self, model, contents, config):
        return FakeResponse(self._parsed_output)
    

class Fakeclient:
    def __init__(self, parsed_output):
        self.models = FakeModels(parsed_output)

class JobLLMScorerTest(unittest.TestCase):
    def setUp(self):
        self.cv_text = 'Math Student with Ai and backend experience'

        self.job = JobPosting(
            id="job-123",
            title="AI Research Intern",
            company="Example Corp",
            location="San Francisco Bay Area",
            url="https://example.com/job/123",
            description="We are looking for an AI intern with Python and ML experience.",
            posted_at=datetime.now(),
        )

    def test_score_job_success(self):
        llm_output = LLMOutput(
            skill_score = 80, 
            experience_score = 70,
            education_score = 90,
            bonus_score = 60,
            apply_recommendation = 'Strong Yes',
            key_reasons = ['Good AI Background', 'Relevant experience'],
            explanation = 'The candidate matchs most of the JD: AI require'
        )
        fake_client = Fakeclient(parsed_output = llm_output)
        scorer = JobLLMScorer(cv_text=self.cv_text, client = fake_client)
        scored_job = scorer.score_job(self.job)

        # Assert
        self.assertIsInstance(scored_job, ScoredJob)
        self.assertEqual(scored_job.job, self.job)
        self.assertEqual(scored_job.skill_score, 80)
        self.assertEqual(scored_job.experience_score, 70)
        self.assertEqual(scored_job.education_score, 90)
        self.assertEqual(scored_job.bonus_score, 60)
        self.assertEqual(scored_job.apply_recommendation, "Strong Yes")
        self.assertIn("AI", scored_job.explanation)

        expected_total = calculate_total_score_from_scores(80, 70, 90, 60)
        self.assertAlmostEqual(scored_job.total_score, expected_total, places=6)



