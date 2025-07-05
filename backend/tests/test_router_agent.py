import unittest
from backend.src.agent.basic.router_agent import RouterAgent

class TestRouterAgent(unittest.TestCase):
    def setUp(self):
        self.agent = RouterAgent()

    def test_decide_agent_returns_valid(self):
        # This is a basic test; in real tests, mock model responses
        result = self.agent.decide_agent("How do I write a for loop in Python?")
        self.assertIn(result, ["code", "simple", "complex"])

if __name__ == "__main__":
    unittest.main()
