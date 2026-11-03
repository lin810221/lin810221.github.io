"""Offline HS256 teaching verifier, not an authorization server or JWKS client."""
import time
import jwt
from mcp.server.auth.provider import AccessToken
from integration_core import Principal

ISSUER = "https://issuer.example.invalid"
RESOURCE = "https://mcp.example.invalid/mcp"
# Public fixture secret. Never use this key or this issuer for production.
DEMO_KEY = "public-course-fixture-key-do-not-use-in-production-2026"


def fixture_token(**overrides) -> str:
    claims = {"iss": ISSUER, "aud": RESOURCE, "sub": "alice", "tenant": "alpha",
              "client_id": "course-client", "scope": "notes:read tickets:read tickets:write",
              "exp": int(time.time()) + 120, "iat": int(time.time())}
    claims.update(overrides)
    return jwt.encode(claims, DEMO_KEY, algorithm="HS256")


class CourseTokenVerifier:
    async def verify_token(self, token: str) -> AccessToken | None:
        try:
            claims = jwt.decode(token, DEMO_KEY, algorithms=["HS256"], audience=RESOURCE,
                                issuer=ISSUER, options={"require": ["exp", "iss", "aud", "sub", "tenant", "client_id"]})
            for key in ("sub", "tenant", "client_id"):
                if not isinstance(claims[key], str) or not claims[key]:
                    return None
            if not isinstance(claims.get("scope", ""), str):
                return None
            return AccessToken(token=token, client_id=claims["client_id"], subject=claims["sub"],
                               resource=RESOURCE, scopes=claims.get("scope", "").split(),
                               expires_at=claims["exp"], claims=claims)
        except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
            return None


def token_principal(token: AccessToken) -> Principal:
    claims = token.claims or {}
    if not token.subject or not claims.get("tenant") or claims.get("iss") != ISSUER:
        raise PermissionError("Verified issuer, subject and tenant are required")
    # OAuth client_id is the calling application, not the human subject.
    return Principal(claims["tenant"], token.subject, frozenset(token.scopes), claims["iss"])
