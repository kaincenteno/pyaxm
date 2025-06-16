import requests
from models import OrgDeviceResponse, MdmServersResponse, MdmServerDevicesLinkagesResponse, OrgDevicesResponse


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

    response = requests.post(
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
        url = 'https://api-business.apple.com/v1/orgDevices'
    headers = {"Authorization": f"Bearer {access_token}"}   
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return OrgDevicesResponse.model_validate(response.json())
    else:
        response.raise_for_status()

def get_device(device_id, access_token) -> OrgDeviceResponse:
    """
    Retrieve an organization device by its ID.
    
    :param device_id: The ID of the organization device to retrieve.
    :param access_token: The access token for authentication.
    :return: An OrgDeviceResponse object containing the device information.
    """

    url = f'https://api-business.apple.com/v1/orgDevices/{device_id}'
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    
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
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return MdmServersResponse.model_validate(response.json())
    else:
        response.raise_for_status()

def list_devices_in_mdm_server(server_id: str, access_token) -> MdmServerDevicesLinkagesResponse:
    """
    List devices in a specific MDM server.
    
    :param server_id: The ID of the MDM server.
    :param access_token: The access token for authentication.
    :return: An MdmServerResponse object containing the MDM server information.
    """
    url = f'https://api-business.apple.com/v1/mdmServers/{server_id}/relationships/devices'
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return MdmServerDevicesLinkagesResponse.model_validate(response.json())
    else:
        response.raise_for_status()
