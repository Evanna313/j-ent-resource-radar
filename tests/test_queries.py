import unittest

from jent_resource_radar.queries import build_search_tasks


class QueryTests(unittest.TestCase):
    def test_builds_expected_sources(self):
        tasks = build_search_tasks(
            "渡辺翔太",
            ["Snow Man", "しょっぴー"],
            "2026年秋冬",
        )
        sources = {task.source for task in tasks}
        self.assertIn("Official / Primary", sources)
        self.assertIn("X live search", sources)
        self.assertIn("Yahoo!リアルタイム", sources)
        self.assertIn("Threads", sources)
        self.assertIn("5ch", sources)
        self.assertIn("Girls Channel", sources)

    def test_urls_are_http(self):
        tasks = build_search_tasks("京本大我", ["SixTONES"], "")
        self.assertTrue(all(task.url.startswith("https://") for task in tasks))


if __name__ == "__main__":
    unittest.main()
