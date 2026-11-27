"""An independent JWT validation lab, not the service's identity provider."""
import jwt


def decode_access_token(token, key, *, issuer='https://issuer.example.test', audience='relaydesk'):
    if len(key) < 32:
        raise ValueError('teaching HS256 secret must contain at least 32 bytes')
    claims = jwt.decode(token, key, algorithms=['HS256'], audience=audience, issuer=issuer, options={'require': ['exp', 'iat', 'sub', 'iss', 'aud']})
    if not isinstance(claims['sub'], str) or not claims['sub'].strip():
        raise ValueError('invalid subject')
    return claims
