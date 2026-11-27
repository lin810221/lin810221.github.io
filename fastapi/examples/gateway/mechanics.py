"""Small runnable experiments that isolate framework behavior from the project."""
import asyncio
from collections.abc import AsyncIterable
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel


def create_mechanics_app():
    app = FastAPI(max_body_size=1024)
    app.state.trace, app.state.active, app.state.peak = [], 0, 0

    async def resource():
        app.state.trace.append('open')
        try:
            yield 'resource'
        finally:
            app.state.trace.append('close')

    async def chunks():
        app.state.trace.append('chunk')
        yield b'one\n'

    @app.get('/function')
    async def function_scope(value: Annotated[str, Depends(resource, scope='function')]):
        app.state.trace.append('route')
        return StreamingResponse(chunks(), media_type='text/plain')

    @app.get('/request')
    async def request_scope(value: Annotated[str, Depends(resource, scope='request')]):
        app.state.trace.append('route')
        return StreamingResponse(chunks(), media_type='text/plain')

    async def slot():
        app.state.active += 1
        app.state.peak = max(app.state.peak, app.state.active)
        try:
            yield
        finally:
            app.state.active -= 1

    limited = Depends(slot, max_concurrency=2)

    @app.get('/limited')
    async def limited_work(value: Annotated[None, limited]):
        await asyncio.sleep(.01)
        return {'ok': True}

    @app.get('/json')
    async def json_input():
        return {'ok': True}

    return app


async def async_database_example():
    from sqlalchemy import text
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
    engine = create_async_engine('sqlite+aiosqlite:///:memory:')
    factory = async_sessionmaker(engine)
    try:
        async with factory() as session, session.begin():
            value = await session.scalar(text('SELECT 6 * 7'))
        return value
    finally:
        await engine.dispose()
