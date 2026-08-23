import unittest
from pathlib import Path

from analytics_agent.agent import InvestigationAgent, percent_change
from analytics_agent.tools import AnalyticsTools


class AgentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tools = AnalyticsTools(Path(__file__).parents[1] / "data" / "sales.csv")

    def test_percent_change(self):
        self.assertEqual(percent_change(80, 100), -20)

    def test_agent_finds_pharmacy(self):
        report = InvestigationAgent(self.tools).investigate("2026-01-14", "2026-01-13")
        self.assertIn("category = Pharmacy", report)
        self.assertIn("Average order value", report)


if __name__ == "__main__":
    unittest.main()

