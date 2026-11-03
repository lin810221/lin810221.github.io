"""Share a concurrency budget across calls; asynchronous does not mean unlimited."""
import asyncio


async def run_batch(count=8, parallelism=2):
    if count < 0 or parallelism < 1:
        raise ValueError("Invalid workload")
    semaphore, active, peak = asyncio.Semaphore(parallelism), 0, 0

    async def one(index):
        nonlocal active, peak
        async with semaphore:
            active += 1
            peak = max(peak, active)
            try:
                async with asyncio.timeout(1):
                    await asyncio.sleep(0.001)  # Fake I/O, never a provider call.
                    return index
            finally:
                active -= 1

    values = await asyncio.gather(*(one(index) for index in range(count)))
    return {"values": values, "peak": peak, "active_after": active}


if __name__ == "__main__":
    print(asyncio.run(run_batch()))
