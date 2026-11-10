# Week 4 Assessment – Rate Limits, Retries, Async and Parallel LLM Calls

## Overview

This project demonstrates how to handle LLM API rate limits, implement automatic retries, and execute asynchronous API requests efficiently using Python.

It covers Tenacity, exponential backoff, asyncio, concurrency control, partial failure handling, and progress tracking.

**Note:** Mock LLM calls are used for demonstration, so an OpenAI API key is not required.

## Project Structure

```text
week4_rate_limits_async/
│
├── task1_retries.py
├── task1_tests.py
├── task2_async.py
├── requirements.txt
└── README.md
```

## Technologies Used

- Python
- Tenacity
- Asyncio
- OpenAI Python SDK
- tqdm
- Unittest

## Task 1 – Rate Limits and Retries

### Objectives

- Implement automatic retries using Tenacity.
- Handle HTTP 429 and 5xx errors.
- Use exponential backoff with a maximum wait of 20 seconds.
- Stop retrying after five attempts.
- Log retry attempt numbers and waiting times.
- Prevent retries for HTTP 400 and 401 errors.

### Implementation

The project uses:

```python
@retry(
    wait=wait_exponential(min=1, max=20),
    stop=stop_after_attempt(5),
    retry=retry_if_exception(should_retry),
    before_sleep=log_retry,
    reraise=True
)
```

### Expected Output

```text
Attempt 1 failed (429) -> wait 1 s
Attempt 2 failed (429) -> wait 2 s
Attempt 3 succeeded
```

### Test Results

- HTTP 400: No retry.
- HTTP 401: No retry.
- HTTP 429: Retry enabled.
- HTTP 5xx: Retry enabled.

## Task 2 – Async and Parallel Calls

### Objectives

- Implement asynchronous LLM calls.
- Execute ten questions sequentially.
- Execute ten questions concurrently.
- Limit concurrency using `asyncio.Semaphore(3)`.
- Handle individual request failures.
- Display progress using `tqdm.asyncio`.
- Compare sequential and parallel execution times.

### Implementation

**Sequential execution:**

Each question is processed one after another.

**Parallel execution:**

`asyncio.gather()` executes multiple asynchronous tasks concurrently.

**Concurrency control:**

```python
semaphore = asyncio.Semaphore(3)
```

**Partial failure handling:**

```python
await tqdm_asyncio.gather(
    *tasks,
    return_exceptions=True
)
```

### Expected Output

```text
Sequential Time: 3.01 seconds
Parallel Time:   1.21 seconds
Speedup:         2.49x
```

*Execution times are illustrative and will vary.*

## Concepts Learned

| Concept | Description |
|---|---|
| HTTP 429 | Too many requests |
| Tenacity | Python retry library |
| Exponential Backoff | Increasing retry delays |
| Jitter | Randomized retry delays |
| Async/Await | Asynchronous programming |
| asyncio.gather | Concurrent task execution |
| Semaphore | Concurrency limitation |
| return_exceptions | Partial failure handling |
| tqdm | Progress visualization |

## Installation and Execution

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd week4_rate_limits_async
```

### 2. Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Task 1

```bash
python task1_retries.py
```

### 5. Run Task 1 tests

```bash
python task1_tests.py
```

### 6. Run Task 2

```bash
python task2_async.py
```

## API Key Requirement

The default implementation uses mock LLM calls and does not require an API key or paid API credits.

An optional `AsyncOpenAI` implementation is included for future integration with the OpenAI API.

## Conclusion

This assessment demonstrates reliable LLM request handling through retry mechanisms and efficient asynchronous execution. It also shows how concurrency limits and exception handling improve the reliability of applications that communicate with LLM APIs.
