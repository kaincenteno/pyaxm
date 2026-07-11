import datetime as dt
import json
import time
import uuid
from dataclasses import dataclass

import jwt


@dataclass
class AccessToken:
    value: str
    expires_at: dt.datetime


class TokenManager:
    """Handles JWT assertion generation and OAuth2 access token lifecycle.

    Creates signed client assertions using an ES256 private key, exchanges
    them for Apple Business Manager OAuth2 tokens, and caches tokens to disk.
    """

    def __init__(
        self,
        abm_requests,
        axm_client_id: str,
        axm_key_id: str,
        key_path: str,
        token_path: str,
    ):
        self._abm = abm_requests
        self.axm_client_id = axm_client_id
        self.axm_key_id = axm_key_id
        self.key_path = key_path
        self.token_path = token_path
        self.access_token = self._get_or_refresh_token()

    def _generate_assertion(self) -> str:
        issued_at = int(dt.datetime.now(dt.timezone.utc).timestamp())
        expires_at = issued_at + 60
        headers = {
            "alg": "ES256",
            "kid": self.axm_key_id,
        }
        payload = {
            "sub": self.axm_client_id,
            "aud": "https://account.apple.com/auth/oauth2/v2/token",
            "iat": issued_at,
            "exp": expires_at,
            "jti": str(uuid.uuid4()),
            "iss": self.axm_client_id,
        }
        with open(self.key_path, "rb") as f:
            key = f.read()
        return jwt.encode(payload, key, algorithm="ES256", headers=headers)

    def _get_or_refresh_token(self) -> AccessToken:
        try:
            with open(self.token_path, "r") as f:
                cache = json.load(f)
            if cache["expires_at"] > time.time():
                value = cache["access_token"]
                expires_at = dt.datetime.fromtimestamp(
                    cache["expires_at"], dt.timezone.utc
                )
                return AccessToken(value, expires_at)
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            pass

        assertion = self._generate_assertion()
        token_data = {
            "grant_type": "client_credentials",
            "client_id": self.axm_client_id,
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": assertion,
            "scope": "business.api",
        }
        token = self._abm.get_access_token(token_data)
        expires_in = token.get("expires_in")
        issued_at = dt.datetime.now(dt.timezone.utc)
        expires_at = issued_at + dt.timedelta(seconds=expires_in)
        value = token.get("access_token")
        cache_data = {
            "access_token": value,
            "expires_at": expires_at.timestamp(),
        }
        with open(self.token_path, "w") as f:
            json.dump(cache_data, f)
        return AccessToken(value, expires_at)

    def ensure_token(self) -> None:
        """Refresh the access token if it has expired or is about to expire."""
        if self.access_token.expires_at <= dt.datetime.now(dt.timezone.utc):
            self.access_token = self._get_or_refresh_token()

    def get_token_value(self) -> str:
        """Return a valid access token value, refreshing if necessary."""
        self.ensure_token()
        return self.access_token.value
