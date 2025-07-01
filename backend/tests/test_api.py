import unittest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

class TestAPI(unittest.TestCase):
    def test_get_models(self):
        response = client.get("/models")
        self.assertEqual(response.status_code, 200)
        self.assertIn("models", response.json())

    def test_ask_question_no_question(self):
        response = client.post("/ask", json={})
        self.assertEqual(response.status_code, 200)
        self.assertIn("error", response.json())

if __name__ == "__main__":
    unittest.main()
