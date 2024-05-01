from os import getenv

from fastapi.security.http import HTTPAuthorizationCredentials
from google.auth import jwt
from icecream import ic


def _token_claims(token: HTTPAuthorizationCredentials) -> dict:
    aud = getenv("AUDIENCE")
    credentials = token.credentials
    claims = jwt.decode(credentials, aud, verify=False)
    if not claims:
        raise ValueError("Invalid token")
    if claims.get("aud") != aud:
        raise ValueError("Invalid audience")
    if claims.get("email_verified") is not True:
        raise ValueError("Email not verified")
    if not claims.get("email"):
        raise ValueError("Email not found in token")
    if not claims.get("sub"):
        raise ValueError("Sub not found in token")
    return claims


def email_and_sub(token: HTTPAuthorizationCredentials) -> tuple[str, str]:
    claims = _token_claims(token)
    return claims["email"], claims["sub"]
