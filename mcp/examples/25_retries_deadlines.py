"""Compute a bounded retry schedule; this simulator never sleeps or calls APIs."""


def retry_schedule(*, read_only: bool, has_idempotency: bool, total_budget: float,
                   attempt_timeout: float, max_attempts: int = 3):
    if total_budget <= 0 or attempt_timeout <= 0 or max_attempts < 1:
        raise ValueError("Positive budgets are required")
    retries_allowed = read_only or has_idempotency
    remaining, schedule = total_budget, []
    for index in range(max_attempts if retries_allowed else 1):
        if remaining <= 0:
            break
        timeout = min(attempt_timeout, remaining)
        schedule.append({"attempt": index + 1, "timeout": timeout})
        remaining -= timeout
        backoff = min(0.1 * 2 ** index, remaining)
        remaining -= backoff
    return schedule


if __name__ == "__main__":
    print(retry_schedule(read_only=True, has_idempotency=False, total_budget=2.5, attempt_timeout=1))
    print(retry_schedule(read_only=False, has_idempotency=False, total_budget=2.5, attempt_timeout=1))
    print("Retry only transient failures; a timeout after a write is an unknown outcome.")
