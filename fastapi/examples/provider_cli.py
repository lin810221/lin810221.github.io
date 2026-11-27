"""Inspect a request plan; paid API execution requires explicit --live and model."""
import argparse
import asyncio
import os
import httpx
from gateway.providers import OpenAIProvider


async def run(args):
    docs = [{'id': 1, 'title': 'Synthetic policy', 'text': 'Warranty lasts 12 months.'}]
    if not args.live:
        print({'endpoint': 'https://api.openai.com/v1/responses', 'model': args.model, 'documents': 1, 'max_output_tokens': 1024, 'network': False})
        return
    key = os.environ.get('OPENAI_API_KEY')
    if not key or not args.model:
        raise SystemExit('--live requires OPENAI_API_KEY and an explicit supported model')
    async with httpx.AsyncClient(timeout=5, follow_redirects=False, trust_env=False) as client:
        result = await OpenAIProvider(client, key, args.model, live=True).answer('How long is the warranty?', docs)
    print(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model')
    parser.add_argument('--live', action='store_true')
    asyncio.run(run(parser.parse_args()))
