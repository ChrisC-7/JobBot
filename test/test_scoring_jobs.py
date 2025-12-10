from src.models import JobPosting, ScoredJob 
from src.scoring import calculate_total_score_for_job, skill_weight, experience_weight, education_weight, bounus_weight
from datetime import datetime
import unittest

def make_scored_jobs_with_base_scores(skill_score, experience_score, education_score, bonus_score):
    job_posting = JobPosting(
        id="1",
        title="t",
        company="c",
        location="l",
        url="u",
        description="d",
        posted_at=datetime.now()
    )
    return ScoredJob(
        job=job_posting,
        skill_score=skill_score,
        experience_score=experience_score,
        education_score=education_score,
        bonus_score=bonus_score,
        total_score=0,
        apply_recommendation="",
        key_reasons=[],
        explanation="",
        auto_apply_supported=False
    )

class ScoringJobTest(unittest.TestCase):
    def test_calculates_weighted_total_correctly(self):
        # Arrange
        job = make_scored_jobs_with_base_scores(
            skill_score=80,
            experience_score=70,
            education_score=90,
            bonus_score=60,
        )
        # 0.45*80 + 0.35*70 + 0.15*90 + 0.05*60
        expected_total = skill_weight*80 + experience_weight*70 + education_weight*90 + bounus_weight*60

        # Act
        calculate_total_score_for_job(job)

        # Assert
        self.assertAlmostEqual(job.total_score, expected_total)

    def test_all_zero_scores_give_zero_total(self):
        job = make_scored_jobs_with_base_scores(
            skill_score=0,
            experience_score=0,
            education_score=0,
            bonus_score=0,
        )

        calculate_total_score_for_job(job)

        self.assertEqual(job.total_score, 0)

    def test_all_hundred_scores_give_hundred_total(self):
        job = make_scored_jobs_with_base_scores(
            skill_score=100,
            experience_score=100,
            education_score=100,
            bonus_score=100,
        )

        calculate_total_score_for_job(job)

        self.assertAlmostEqual(job.total_score, 100.0)

if __name__ == "__main__":
    unittest.main()
