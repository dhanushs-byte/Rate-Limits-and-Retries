
import unittest
from task1_retries import APIError, llm_call


class FailingLLM:
    def __init__(self, status_code):
        self.status_code = status_code
        self.attempts = 0

    def call(self, prompt):
        self.attempts += 1
        raise APIError(self.status_code)


class RetryTests(unittest.TestCase):

    def test_400_not_retried(self):
        client = FailingLLM(400)

        with self.assertRaises(APIError):
            llm_call(client, "Test")

        self.assertEqual(client.attempts, 1)
        print("PASS: 400 error was not retried")

    def test_401_not_retried(self):
        client = FailingLLM(401)

        with self.assertRaises(APIError):
            llm_call(client, "Test")

        self.assertEqual(client.attempts, 1)
        print("PASS: 401 error was not retried")


if __name__ == "__main__":
    unittest.main()
