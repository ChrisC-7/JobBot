import unittest
from src.models import JobPosting, ScoredJob
from datetime import datetime
from src.rankingJobs import rankedJobs
def make_scored_job(score:float):
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
        job = job_posting,
        skill_score = 0,
        experience_score = 0,
        education_score=0,
        bonus_score = 0,
        total_score = score,
        apply_recommendation = "",
        key_reasons = [],
        explanation = "",
        auto_apply_supported = False
    )

class RankedJobsTest(unittest.TestCase):

    def test_filters_out_low_scores(self):
        jobs = [make_scored_job(60), make_scored_job(30), make_scored_job(80)]
        result = rankedJobs(jobs)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(job.total_score >= 60 for job in result))

    def test_sorts_in_descending_order(self):
        jobs = [make_scored_job(60), make_scored_job(90), make_scored_job(75)]
        result = rankedJobs(jobs)
        scores = [job.total_score for job in result]
        self.assertEqual(scores, sorted(scores, reverse=True))
    
    def test_limits_to_max_jobs(self):
        jobs = [make_scored_job(90) for _ in range(50)]  # 50 high score jobs
        result = rankedJobs(jobs)
        self.assertEqual(len(result), 30)  # max_jobs_per_day

if __name__ == "__main__":
    unittest.main()
