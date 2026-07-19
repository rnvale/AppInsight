import sys
import unittest
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app import app  # noqa: E402


class AnalyticsContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(TESTING=True)
        cls.client = app.test_client()

    def test_api_meta_reports_appinsight_4(self):
        response = self.client.get("/api/meta")

        self.assertEqual(response.status_code, 200)
        self.assertIn("AppInsight API v4.0", response.get_json()["name"])

    def test_sentiment_filter_keeps_comparison_distribution(self):
        response = self.client.post("/api/rating_sentiment", json={"sentiment": "positive"})

        self.assertEqual(response.status_code, 200)
        rows = response.get_json()
        self.assertTrue(any(row["negative"] > 0 for row in rows))
        self.assertTrue(all("sample_size" in row for row in rows))
        self.assertTrue(all("rate_low" in row and "rate_high" in row for row in rows))

    def test_summary_total_matches_labeled_sentiment_records(self):
        response = self.client.post("/api/summary", json={"sentiment": "all"})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["total"], payload["positive"] + payload["negative"])
        self.assertGreaterEqual(payload["record_total"], payload["total"])

    def test_heatmap_exposes_both_sentiments_and_sample_size(self):
        response = self.client.post("/api/emotion_heatmap", json={"sentiment": "all"})

        self.assertEqual(response.status_code, 200)
        row = response.get_json()[0]
        self.assertIn("negative_rate", row)
        self.assertIn("sentiment_balance", row)
        self.assertIn("sample_size", row)

    def test_quadrant_returns_data_and_dynamic_cut_lines(self):
        response = self.client.post("/api/quadrant_scatter", json={"sentiment": "all"})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIsInstance(payload, dict)
        self.assertIn("data", payload)
        self.assertIn("mid_positive_rate", payload)
        self.assertIn("mid_reviews", payload)


if __name__ == "__main__":
    unittest.main()
