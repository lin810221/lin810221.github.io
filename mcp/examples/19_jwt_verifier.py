"""Reject a correctly signed token whose audience is for another service."""
import anyio
from auth_verifier import CourseTokenVerifier, fixture_token, token_principal


async def main():
    verifier = CourseTokenVerifier()
    accepted = await verifier.verify_token(fixture_token())
    assert accepted is not None
    principal = token_principal(accepted)
    assert await verifier.verify_token(fixture_token(aud="https://other.example.invalid")) is None
    assert await verifier.verify_token(fixture_token(exp=1)) is None
    print("verified subject", principal.subject, "tenant", principal.tenant)
    print("wrong audience / expired token: rejected")  # Never print token values.


if __name__ == "__main__":
    anyio.run(main)
