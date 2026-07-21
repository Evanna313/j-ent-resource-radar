import unittest

from jent_resource_radar.models import EvidenceTier, Finding


class FindingTests(unittest.TestCase):
    def test_parses_valid_finding(self):
        finding = Finding.from_dict(
            {
                "tier": "d",
                "headline": "Rumor",
                "source_name": "Forum",
                "url": "https://example.com",
                "published_at": "2026-07-21",
                "summary": "Unverified claim.",
                "status": "unclear",
            }
        )
        self.assertEqual(finding.tier, EvidenceTier.D)
        self.assertEqual(finding.status, "unclear")

    def test_rejects_missing_fields(self):
        with self.assertRaises(ValueError):
            Finding.from_dict({"tier": "A"})


if __name__ == "__main__":
    unittest.main()
