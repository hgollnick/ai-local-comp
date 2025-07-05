import unittest
from backend.src.agent.basic.router_agent import RouterAgent

class TestRouterAgent(unittest.TestCase):
    def test_router_agent_instantiation(self):
        try:
            agent = RouterAgent()
            self.assertIsNotNone(agent)
        except Exception as e:
            self.fail(f"RouterAgent instantiation failed: {e}")

if __name__ == "__main__":
    unittest.main()
