import requests
from pyaxm.models import OrgDeviceResponse, MdmServersResponse, MdmServerDevicesLinkagesResponse, OrgDevicesResponse
import time

# creating a session to reuse connections
# didn't really improved performance, should revert back 
# to requests without session?
session = requests.Session()

def _auth_headers(access_token: str) -> dict:
    """
    :param access_token: The access token for authentication.
    :return: A dictionary containing the authorization headers.
    """
    return {"Authorization": f"Bearer {access_token}"}

def get_access_token(data: dict) -> dict:
    """
    Generate an access token for Apple Business Manager API.
    :param data: A dictionary containing the necessary parameters for the token request.
    :return: A dictionary containing the access token and other related information.
    """
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'account.apple.com'
    }

    response = session.post(
        'https://account.apple.com/auth/oauth2/token',
        headers=headers,
        data=data
    )

    response.raise_for_status()
    return response.json()

def list_devices(access_token, next=None) -> OrgDevicesResponse:
    """
    List all organization devices.
    :param access_token: The access token for authentication.
    :param next: Optional; the URL for the next page of results.
    :return: An OrgDevicesResponse object containing the list of devices.
    """
    if next:
        url = next
    else:
        # Default is 100 devices. Documentation says max is 1000 but 
        # currently querying a unspecified number returns status code 500
        # increase this when apple fixes the issue to 1000
        url = 'https://api-business.apple.com/v1/orgDevices'

    retries = 3
    for attempt in range(retries):
        response = session.get(url, headers=_auth_headers(access_token))

        # ABM has been returning 500, this is a workaround to retry 2 times
        # before raising an error.
        if response.status_code != 200:
            if attempt < retries - 1:
                time.sleep(5)
                continue
            else:
                print(response.text)
                response.raise_for_status()   
        else:
            return OrgDevicesResponse.model_validate(response.json())

def get_device(device_id, access_token) -> OrgDeviceResponse:
    """
    Retrieve an organization device by its ID.
    
    :param device_id: The ID of the organization device to retrieve.
    :param access_token: The access token for authentication.
    :return: An OrgDeviceResponse object containing the device information.
    """

    url = f'https://api-business.apple.com/v1/orgDevices/{device_id}'
    response = session.get(url, headers=_auth_headers(access_token))
    
    if response.status_code == 200:
        return OrgDeviceResponse.model_validate(response.json())
    else:
        response.raise_for_status()

def list_mdm_servers(access_token) -> MdmServersResponse:
    """
    List all MDM servers.
    
    :param access_token: The access token for authentication.
    :return: An MdmServersResponse object containing the list of MDM servers.
    """
    url = 'https://api-business.apple.com/v1/mdmServers'    
    response = session.get(url, headers=_auth_headers(access_token))
    
    if response.status_code == 200:
        return MdmServersResponse.model_validate(response.json())
    else:
        response.raise_for_status()

def list_devices_in_mdm_server(server_id: str, access_token, next=None) -> MdmServerDevicesLinkagesResponse:
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

    retries = 3
    for attempt in range(retries):
        response = session.get(url, headers=_auth_headers(access_token))

        # ABM has been returning 500, this is a workaround to retry 2 times
        # before raising an error.
        if response.status_code != 200:
            if attempt < retries - 1:
                time.sleep(5)
                continue
            else:
                print(response.text)
                response.raise_for_status()
        else:
            return MdmServerDevicesLinkagesResponse.model_validate(response.json())
