import datetime as dt
import Cryptodome.PublicKey.ECC as ECC
from authlib.jose import jwt
import uuid
import os
import json
import time
from pyaxm.abm_requests import ABMRequests
from functools import wraps

ABM_CLIENT_ID = os.environ['AXM_CLIENT_ID']
ABM_KEY_ID = os.environ['AXM_KEY_ID']
ABM_FOLDER = os.path.join(os.path.expanduser('~'), '.config', 'pyaxm')
KEY_PATH = os.path.join(ABM_FOLDER, 'key.pem')
TOKEN_PATH = os.path.join(ABM_FOLDER, 'token.json')

class AccessToken:
    def __init__(self, value, expires_at):
        self.value = value
        self.expires_at = expires_at

def ensure_valid_token(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.access_token.expires_at <= dt.datetime.now(dt.timezone.utc):
            self.access_token = self._get_or_refresh_token()
        return method(self, *args, **kwargs)
    return wrapper

class Client:
    def __init__(self):
        self.abm = ABMRequests()
        self.access_token = self._get_or_refresh_token()

    def _get_or_refresh_token(self):
        try:
            with open(TOKEN_PATH, 'r') as f:
                cache = json.load(f)
            if cache['expires_at'] > time.time():
                value = cache['access_token']
                expires_at = dt.datetime.fromtimestamp(cache['expires_at'], dt.timezone.utc)
                return AccessToken(value, expires_at)
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            pass
        # Generate new token
        assertion = self._generate_assertion()
        token_data = {
            "grant_type": "client_credentials",
            "client_id": ABM_CLIENT_ID,
            "client_assertion_type": 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            "client_assertion": assertion,
            "scope": 'business.api'
        }
        token = self.abm.get_access_token(token_data)
        expires_in = token.get('expires_in')
        issued_at = dt.datetime.now(dt.timezone.utc)
        expires_at = issued_at + dt.timedelta(seconds=expires_in)
        value = token.get('access_token')
        cache_data = {
            'access_token': value,
            'expires_at': expires_at.timestamp()
        }
        with open(TOKEN_PATH, 'w') as f:
            json.dump(cache_data, f)
        return AccessToken(value, expires_at)

    def _generate_assertion(self):
        issued_at = int(dt.datetime.now(dt.timezone.utc).timestamp())
        expires_at = issued_at + 60
        headers = {
            "alg": "ES256",
            "kid": ABM_KEY_ID
        }
        payload = {
            "sub": ABM_CLIENT_ID,
            "aud": 'https://account.apple.com/auth/oauth2/v2/token',
            "iat": issued_at,
            "exp": expires_at,
            "jti": str(uuid.uuid4()),
            "iss": ABM_CLIENT_ID
        }
        with open(KEY_PATH, 'rt') as f:
            private_key = ECC.import_key(f.read())
        assertion = jwt.encode(
            header=headers,
            payload=payload,
            key=private_key.export_key(format='PEM')
        ).decode("utf-8")
        return assertion

    @ensure_valid_token
    def list_devices(self) -> list[dict]:
        response = self.abm.list_devices(self.access_token.value)
        devices = [data.attributes.model_dump() for data in response.data]
        while response.links.next:
            next_page = response.links.next
            response = self.abm.list_devices(self.access_token.value, next=next_page)
            devices.extend([data.attributes.model_dump() for data in response.data])
        return devices

    @ensure_valid_token
    def get_device(self, device_id: str) -> dict:
        response = self.abm.get_device(device_id, self.access_token.value)
        return response.data.attributes.model_dump()
    
    @ensure_valid_token
    def list_mdm_servers(self) -> list[dict]:
        response = self.abm.list_mdm_servers(self.access_token.value)
        exclude_keys = {
            'data': {
                '__all__': {
                    'relationships',
                    'type'
                },
            },
            'included': True,
            'links': True,
            'meta': True,
        }
        data = response.model_dump(exclude=exclude_keys)
        data = [
            {
                'id': server.id,
                'createdDateTime': server.attributes.createdDateTime,
                'serverName': server.attributes.serverName,
                'serverType': server.attributes.serverType,
                'updatedDateTime': server.attributes.updatedDateTime
            } for server in response.data
        ]
        return data

    @ensure_valid_token
    def list_devices_in_mdm_server(self, server_id: str) -> list[str]:
        response = self.abm.list_devices_in_mdm_server(server_id, self.access_token.value)
        include_keys= {
            'data': {
                '__all__': {
                    'id'
                }
            }
        }
        devices = response.model_dump(include=include_keys)
        devices = [device for device in devices['data']]
        while response.links.next:
            next_page = response.links.next
            response = self.abm.list_devices_in_mdm_server(server_id, self.access_token.value, next=next_page)
            devices_dump = response.model_dump(include=include_keys)
            devices_dump = [device for device in devices_dump['data']]
            devices.extend(devices_dump)
        return devices

    @ensure_valid_token
    def get_device_server_assignment(self, device_id: str) -> dict:
        response = self.abm.get_device_server_assignment(device_id, self.access_token.value)
        include_keys = {
            'id'
        }
        return response.data.model_dump(include=include_keys)

    @ensure_valid_token
    def assign_unassign_device_to_mdm_server(
        self, device_id: str, server_id: str, action: str
    ) -> None:
        """
        Assign or unassign a device to/from an MDM server.

        :param device_id: The ID of the device.
        :param server_id: The ID of the MDM server.
        :param action: 'assign' or 'unassign'.
        """
        unassign_response = self.abm.assign_unassign_device_to_mdm_server(
            device_id, server_id, action, self.access_token.value
        )

        # use the ID to check the status until it is complete
        activity_response = self.abm.get_device_activity(unassign_response.data.id, self.access_token.value)
        retry = 0
        while 'COMPLETED' not in activity_response.data.attributes.status and retry < 5:
            time.sleep(2 ** retry)
            retry += 1
            activity_response = self.abm.get_device_activity(unassign_response.data.id, self.access_token.value)

        return activity_response.data.attributes.model_dump()
