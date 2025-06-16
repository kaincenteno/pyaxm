
import datetime as dt
from models import OrgDevice
import abm_requests as abm_requests
import datetime as dt
import Cryptodome.PublicKey.ECC as ECC
from authlib.jose import jwt
import uuid
import os
import json
import time

ABM_CLIENT_ID = os.environ['ABM_CLIENT_ID']
ABM_KEY_ID = os.environ['ABM_KEY_ID']
ABM_FOLDER = os.path.join(os.path.expanduser('~'), '.config', 'pyabm')
KEY_PATH = os.path.join(ABM_FOLDER, 'key.pem')
TOKEN_PATH = os.path.join(ABM_FOLDER, 'token.json')

class AccessToken():
    def __init__(self):
        self.value = None
        self.expires_at = None
        self.assertion = None

        # Try reading from cache
        try:
            with open(TOKEN_PATH, 'r') as f:
                cache = json.load(f)
            
            if cache['expires_at'] > time.time():
                self.value = cache['access_token']
                self.expires_at = dt.datetime.fromtimestamp(cache['expires_at'], dt.timezone.utc)  # Convert timestamp back to datetime
                return
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            pass
        
        # Get new token
        self.generate_assertion()
        self.generate_token()

        # Write to cache
        cache_data = {
            'access_token': self.value,
            'expires_at': (self.expires_at).timestamp()  # Store as a timestamp
        }

        with open(TOKEN_PATH, 'w') as f:
            json.dump(cache_data, f)
    
    def generate_assertion(self):
        issued_at = int(dt.datetime.now(dt.timezone.utc).timestamp())
        expires_at = issued_at + 60 # expires in 1 minute

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

        self.assertion = jwt.encode(
            header=headers,
            payload=payload,
            key=private_key.export_key(format='PEM')
        ).decode("utf-8")

    def generate_token(self):     
        data = {
            "grant_type": "client_credentials",
            "client_id": ABM_CLIENT_ID,
            "client_assertion_type": 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            "client_assertion": self.assertion,
            "scope": 'business.api'
        }

        token = abm_requests.get_access_token(data)        
        expires_in = token.get('expires_in')
        issued_at = dt.datetime.now(dt.timezone.utc)

        self.expires_at = issued_at + dt.timedelta(seconds=expires_in)
        self.value = token.get('access_token')

class Client:
    def __init__(self):
        self.access_token = AccessToken()
    
    def list_devices(self) -> list[OrgDevice]:
        '''Returns a list of devices in the organization.
        '''
        response = abm_requests.list_devices(self.access_token)
        devices = response.data
        count = 1

        while response.links.next:
            count += 1
            print(f"Fetching page {count} of devices...")
            next_page = response.links.next
            response = abm_requests.list_devices(self.access_token.value, next=next_page)
            devices.extend(response.data)
            
        return devices


    def get_device(self, device_id: str) -> OrgDevice:
        response = abm_requests.get_device(device_id, self.access_token.value)
        return response.data

    ## - MDM servers
    def list_mdm_servers(self) -> list[dict]:
        '''Returns a list of MDM servers with their names and IDs.
        TODO: Add pagination as currently it only returns the first page of results.
        '''
        response = abm_requests.list_mdm_servers(self.access_token.value)
        return [{'server_name': data.attributes.serverName, 'server_id': data.id} for data in response.data]

    ## - list_devices_in_mdm_server
    def list_devices_in_mdm_server(self, server_id: str) -> list[str]:
        '''Returns a list of device IDs (serials) in the specified MDM server.
        TODO: Add pagination as currently it only returns the first page of results.'''
        response = abm_requests.list_devices_in_mdm_server(server_id, self.access_token.value)
        return [data.id for data in response.data]
