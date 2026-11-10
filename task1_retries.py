
import logging
from tenacity import (
    retry,
    wait_exponential,
    stop_after_attempt,
    retry_if_exception,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)


# Custom API exception
class APIError(Exception):
    def __init__(self, status_code):
        self.status_code = status_code
        super().__init__(f"API Error: {status_code}")


# Retry only for 429 and 5xx
def should_retry(exception):
    return (
        isinstance(exception, APIError)
        and (
            exception.status_code == 429
            or 500 <= exception.status_code <= 599
        )
    )


# Log every retry and waiting time
def log_retry(retry_state):
    exception = retry_state.outcome.exception()
    attempt = retry_state.attempt_number
    wait_time = retry_state.next_action.sleep

    logging.info(
        f"Attempt {attempt} failed "
        f"({exception.status_code}) -> wait {wait_time:g} s"
    )


# Mock LLM that fails twice, then succeeds
class MockLLM:
    def __init__(self):
        self.attempts = 0

    def call(self, prompt):
        self.attempts += 1

        if self.attempts <= 2:
            raise APIError(429)

        return "LLM Response: " + prompt


@retry(
    wait=wait_exponential(min=1, max=20),
    stop=stop_after_attempt(5),
    retry=retry_if_exception(should_retry),
    before_sleep=log_retry,
    reraise=True
)
def llm_call(client, prompt):
    return client.call(prompt)


if __name__ == "__main__":
    print("TASK 1: RATE LIMITS AND RETRIES")

    client = MockLLM()

    try:
        result = llm_call(client, "Explain Machine Learning")
        print(f"Attempt {client.attempts} succeeded")
        print(result)

    except APIError as error:
        print("Request failed:", error)
