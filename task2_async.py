
import asyncio
import time
from tqdm.asyncio import tqdm_asyncio


QUESTIONS = [
    "What is Python?",
    "Explain Machine Learning",
    "What is Deep Learning?",
    "Explain Neural Networks",
    "What is NLP?",
    "Explain Transformers",
    "What is RAG?",
    "Explain LLMs",
    "What are embeddings?",
    "Explain AI agents?"
]

# Store individual execution times
execution_times = {}


# Mock asynchronous LLM call
async def ask(q):
    start = time.perf_counter()

    try:
        await asyncio.sleep(0.3)

        # Simulate one failed API request
        if q == "Explain Transformers":
            raise Exception("Simulated API failure")

        return f"Answer for: {q}"

    finally:
        execution_times[q] = time.perf_counter() - start


# Sequential execution
async def run_sequential():
    print("\nSEQUENTIAL EXECUTION")

    results = []

    start = time.perf_counter()

    for q in QUESTIONS:
        try:
            result = await ask(q)
            results.append((q, "Success", execution_times[q]))
        except Exception:
            results.append((q, "Failed", execution_times[q]))

    total_time = time.perf_counter() - start

    return results, total_time


# Parallel execution with semaphore
async def run_parallel():
    print("\nPARALLEL EXECUTION")

    semaphore = asyncio.Semaphore(3)

    async def limited_ask(q):
        async with semaphore:
            return await ask(q)

    start = time.perf_counter()

    tasks = [
        limited_ask(q) for q in QUESTIONS
    ]

    # Progress bar and partial failure handling
    responses = await tqdm_asyncio.gather(
        *tasks,
        return_exceptions=True,
        desc="Processing Questions"
    )

    total_time = time.perf_counter() - start

    results = []

    for q, response in zip(QUESTIONS, responses):
        status = "Failed" if isinstance(response, Exception) else "Success"

        results.append(
            (q, status, execution_times[q])
        )

    return results, total_time


# Print results table
def print_table(results):
    print("\n{:<30} {:<12} {:<12}".format(
        "Question", "Status", "Time (s)"
    ))

    print("-" * 55)

    for question, status, elapsed in results:
        print("{:<30} {:<12} {:.3f}".format(
            question, status, elapsed
        ))


async def main():
    print("TASK 2: ASYNC AND PARALLEL LLM CALLS")

    sequential_results, sequential_time = await run_sequential()

    print_table(sequential_results)

    # Reset timings before parallel execution
    execution_times.clear()

    parallel_results, parallel_time = await run_parallel()

    print_table(parallel_results)

    print("\nPERFORMANCE COMPARISON")
    print(f"Sequential Time: {sequential_time:.2f} seconds")
    print(f"Parallel Time:   {parallel_time:.2f} seconds")

    if parallel_time > 0:
        speedup = sequential_time / parallel_time
        print(f"Speedup:         {speedup:.2f}x")




semaphore = asyncio.Semaphore(3)


async def ask_openai(q):
    async with semaphore:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": q}
            ]
        )

        return response.choices[0].message.content

if __name__ == "__main__":
    asyncio.run(main())
