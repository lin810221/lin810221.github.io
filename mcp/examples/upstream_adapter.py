"""Bounded HTTP result parsing. Caller owns the reviewed base URL and client."""
import json
from typing import Literal
from pydantic import BaseModel, ConfigDict


class ServiceStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")
    service: str
    status: Literal["ok", "degraded"]


async def fetch_status(http, *, max_bytes=4096) -> ServiceStatus:
    chunks, size = [], 0
    # Fixed relative path: the model cannot choose an arbitrary URL.
    async with http.stream("GET", "/status", timeout=3, follow_redirects=False) as response:
        if response.status_code != 200:
            raise ValueError("Upstream did not return a successful status response")
        if response.headers.get("content-type", "").split(";", 1)[0].strip() != "application/json":
            raise ValueError("Upstream content type is not JSON")
        async for chunk in response.aiter_bytes():
            size += len(chunk)
            if size > max_bytes:
                raise ValueError("Upstream result exceeds the byte budget")
            chunks.append(chunk)
    return ServiceStatus.model_validate(json.loads(b"".join(chunks)))
