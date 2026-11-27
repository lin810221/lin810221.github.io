import asyncio
import time
from .providers import ExtractiveProvider, validate_answer
from .store import DomainError


class InjectedCrash(RuntimeError):
    pass


async def run_once(store, provider=None, *, clock=None, crash_before_publish=False):
    now = clock or (lambda: int(time.time()))
    claim = await asyncio.to_thread(store.claim, now())
    if claim is None:
        return None
    provider = provider or ExtractiveProvider()
    try:
        if (await asyncio.to_thread(store.job, claim['tenant'], claim['id']))['cancel_requested']:
            return await asyncio.to_thread(store.finish, claim, {'status': 'abstained', 'text': 'Cancelled before provider invocation.', 'citations': []}, now())
        documents = await asyncio.to_thread(store.selected, claim['tenant'], claim['request']['document_ids'])
        async with asyncio.timeout(15):
            value = await provider.answer(claim['request']['question'], documents)
        result = validate_answer(value, documents, extractive=isinstance(provider, ExtractiveProvider))
        if crash_before_publish:
            raise InjectedCrash('simulated process death before publication')
        return await asyncio.to_thread(store.finish, claim, result, now())
    except InjectedCrash:
        raise  # Leave the lease for an independently restarted worker.
    except DomainError as exc:
        if exc.code == 'stale_lease':
            return {'id': claim['id'], 'state': 'stale'}
        await asyncio.to_thread(store.fail, claim, now())
        raise
    except Exception:
        await asyncio.to_thread(store.fail, claim, now())
        raise
