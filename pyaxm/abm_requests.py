import requests
from pyaxm.models import (
    OrgDeviceResponse,
    MdmServersResponse,
    MdmServerDevicesLinkagesResponse,
    OrgDevicesResponse,
    OrgDeviceAssignedServerLinkageResponse,
)
import time
from functools import wraps

def exponential_backoff(retries=5, backoff_factor=2):
    """
    A decorator for retrying a function with exponential backoff.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    if attempt < retries - 1:
                        wait_time = backoff_factor ** attempt
                        time.sleep(wait_time)
                    else:
                        raise e
        return wrapper
    return decorator

class DeviceError(Exception):
    pass

class ABMRequests:
    def __init__(self):
        self.session = requests.Session()

    @staticmethod
    def _auth_headers(access_token: str) -> dict:
        """
        :param access_token: The access token for authentication.
        :return: A dictionary containing the authorization headers.
        """
        return {"Authorization": f"Bearer {access_token}"}

    def get_access_token(self, data: dict) -> dict:
        """
        Generate an access token for Apple Business Manager API.
        :param data: A dictionary containing the necessary parameters for the token request.
        :return: A dictionary containing the access token and other related information.
        """
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'account.apple.com'
        }

        response = self.session.post(
            'https://account.apple.com/auth/oauth2/token',
            headers=headers,
            data=data
        )

        response.raise_for_status()
        return response.json()

    @exponential_backoff(retries=5, backoff_factor=2)
    def list_devices(self, access_token, next=None) -> OrgDevicesResponse:
        """
        List all organization devices.
        :param access_token: The access token for authentication.
        :param next: Optional; the URL for the next page of results.
        :return: An OrgDevicesResponse object containing the list of devices.
        """
        if next:
            url = next
        else:
            url = 'https://api-business.apple.com/v1/orgDevices?limit=1000'

        response = self.session.get(url, headers=self._auth_headers(access_token))

        if response.status_code == 200:
            return OrgDevicesResponse.model_validate(response.json())
        else:
            response.raise_for_status()

    @exponential_backoff(retries=5, backoff_factor=2)
    def get_device(self, device_id, access_token) -> OrgDeviceResponse:
        """
        Retrieve an organization device by its ID.
        
        :param device_id: The ID of the organization device to retrieve.
        :param access_token: The access token for authentication.
        :return: An OrgDeviceResponse object containing the device information.
        """

        url = f'https://api-business.apple.com/v1/orgDevices/{device_id}'
        response = self.session.get(url, headers=self._auth_headers(access_token))
        
        if response.status_code == 200:
            return OrgDeviceResponse.model_validate(response.json())
        elif response.status_code == 404:
            raise DeviceError(response.json()['errors'][0]['title'])
        else:
            response.raise_for_status()

    @exponential_backoff(retries=5, backoff_factor=2)
    def list_mdm_servers(self, access_token) -> MdmServersResponse:
        """
        List all MDM servers.
        
        :param access_token: The access token for authentication.
        :return: An MdmServersResponse object containing the list of MDM servers.
        """
        url = 'https://api-business.apple.com/v1/mdmServers'    
        response = self.session.get(url, headers=self._auth_headers(access_token))
        
        if response.status_code == 200:
            return MdmServersResponse.model_validate(response.json())
        else:
            response.raise_for_status()

    @exponential_backoff(retries=5, backoff_factor=2)
    def list_devices_in_mdm_server(self, server_id: str, access_token, next=None) -> MdmServerDevicesLinkagesResponse:
        """
        List devices in a specific MDM server.
        
        :param server_id: The ID of the MDM server.
        :param access_token: The access token for authentication.
        :param next: Optional; the URL for the next page of results.
        :return: An MdmServerResponse object containing the MDM server information.
        """
        if next:
            url = next
        else:
            url = f'https://api-business.apple.com/v1/mdmServers/{server_id}/relationships/devices?limit=1000'

        response = self.session.get(url, headers=self._auth_headers(access_token))

        # ABM has been returning 500, this is a workaround to retry 2 times
        # before raising an error.
        if response.status_code == 200:
            return MdmServerDevicesLinkagesResponse.model_validate(response.json())
        else:
            response.raise_for_status()

    @exponential_backoff(retries=5, backoff_factor=2)
    def get_device_server_assignment(self, device_id, access_token) -> OrgDeviceAssignedServerLinkageResponse:
        '''Get the server id that a device is assigned to
        '''
        url = f'https://api-business.apple.com/v1/orgDevices/{device_id}/relationships/assignedServer'
        response = self.session.get(url, headers=self._auth_headers(access_token))
        
        if response.status_code == 200:
            return OrgDeviceAssignedServerLinkageResponse.model_validate(response.json())
        elif response.status_code == 404:
            raise DeviceError(response.json()['errors'][0]['title'])
        else:
            response.raise_for_status()
