"""Authenticated ASGI fixture; uses a PUBLIC demo signing key, never deploy it.

This verifies the resource-server boundary. An actual identity provider, login,
JWKS rotation and production HTTPS setup are deliberately outside this fixture.
"""
from pydantic import AnyHttpUrl
from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.auth.settings import AuthSettings
from auth_verifier import CourseTokenVerifier, ISSUER, RESOURCE, token_principal
from capstone_server import build_capstone


def current_principal():
    token = get_access_token()
    if token is None:
        raise PermissionError("An authenticated HTTP principal is required")
    return token_principal(token)


def build_protected_server(store):
    return build_capstone(store, current_principal,
        token_verifier=CourseTokenVerifier(),
        auth=AuthSettings(issuer_url=AnyHttpUrl(ISSUER), resource_server_url=AnyHttpUrl(RESOURCE),
                          required_scopes=["notes:read"], validate_token_resource=True))
