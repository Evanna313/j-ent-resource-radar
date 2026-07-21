import unittest

from jent_resource_radar.models import Finding
from jent_resource_radar.report import render_report


class ReportTests(unittest.TestCase):
    def test_empty_report_is_cautious(self):
        report = render_report("Example Artist", "2026年秋冬", [])
        self.assertIn("没有发现有意义的新进展", report)
        self.assertIn("不等于艺人没有未公开工作", report)

    def test_official_finding_is_grouped(self):
        finding = Finding.from_dict(
            {
                "tier": "A",
                "headline": "Official announcement",
                "source_name": "TV Network",
                "url": "https://example.com",
                "published_at": "2026-07-21",
                "summary": "A role was officially announced.",
                "status": "new",
            }
        )
        report = render_report("Example Artist", "2026年秋冬", [finding])
        self.assertIn("新的官方确认", report)
        self.assertIn("Official announcement", report)


if __name__ == "__main__":
    unittest.main()
