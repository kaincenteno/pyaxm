import requests
from http import HTTPStatus
from typing import List, Optional
from pyaxm.models import (
    OrgDeviceResponse,
    MdmServersResponse,
    MdmServerDevicesLinkagesResponse,
    OrgDevicesResponse,
    OrgDeviceAssignedServerLinkageResponse,
    OrgDeviceActivityCreateRequest,
    OrgDeviceActivityResponse,
    OrgDeviceActivityType,
    AppleCareCoverageResponse,
    AuditEventsResponse,
    UsersResponse,
    UserResponse,
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
                    if e.response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                        wait_time = int(e.response.headers.get('Retry-After', 60))
                    elif attempt < retries - 1:
                        wait_time = backoff_factor ** attempt
                    else:
                        raise e
                    time.sleep(wait_time)
        return wrapper
    return decorator

class DeviceError(Exception):
    pass

class UserError(Exception):
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

        if response.status_code == HTTPStatus.OK:
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
        
        if response.status_code == HTTPStatus.OK:
            return OrgDeviceResponse.model_validate(response.json())
        elif response.status_code == HTTPStatus.NOT_FOUND:
            raise DeviceError(response.json()['errors'][0]['title'])
        else:
            response.raise_for_status()

    @exponential_backoff(retries=5, backoff_factor=2)
    def get_audit_events(
        self,
        access_token: str,
        start_timestamp: str,
        end_timestamp: str,
        actor_id: str = None,
        subject_id: str = None,
        event_type: str = None,
        limit: int = None,
        fields: List[str] = None,
        cursor: str = None,
        next: str = None,
    ) -> AuditEventsResponse:
        """
        Get a list of audit events in an organization that satisfies the query criteria.

        :param access_token: The access token for authentication.
        :param start_timestamp: ISO8601 formatted start timestamp of query time range.
        :param end_timestamp: ISO8601 formatted end timestamp of query time range.
        :param actor_id: Id of actor of event.
        :param subject_id: Id of subject of event.
        :param event_type: Type of event.
        :param limit: The number of included related resources to return. Maximum: 1000.
        :param fields: Specific fields to return, e.g., ['eventDateTime', 'type'].
        :param cursor: Opaque cursor for pagination.
        :return: An AuditEventsResponse object containing the list of audit events.
        """

        if next:
            url = next
        else:
            url = 'https://api-business.apple.com/v1/auditEvents'

        params = {
            'filter[startTimestamp]': start_timestamp,
            'filter[endTimestamp]': end_timestamp,
        }

        if actor_id:
            params['filter[actorId]'] = actor_id
        if subject_id:
            params['filter[subjectId]'] = subject_id
        if event_type:
            params['filter[type]'] = event_type
        if limit:
            params['limit'] = limit
        if fields:
            params['fields[auditEvents]'] = ','.join(fields)
        if cursor:
            params['cursor'] = cursor

        response = self.session.get(
            url,
            headers=self._auth_headers(access_token),
            params=None if next else params
        )
        if response.status_code == HTTPStatus.OK:
            return AuditEventsResponse.model_validate(response.json())
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
        
        if response.status_code == HTTPStatus.OK:
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

        if response.status_code == HTTPStatus.OK:
            return MdmServerDevicesLinkagesResponse.model_validate(response.json())
        else:
            response.raise_for_status()

    @exponential_backoff(retries=5, backoff_factor=2)
    def get_device_server_assignment(self, device_id, access_token) -> OrgDeviceAssignedServerLinkageResponse:
        '''Get the server id that a device is assigned to
        '''
        url = f'https://api-business.apple.com/v1/orgDevices/{device_id}/relationships/assignedServer'
        response = self.session.get(url, headers=self._auth_headers(access_token))
        
        if response.status_code == HTTPStatus.OK:
            return OrgDeviceAssignedServerLinkageResponse.model_validate(response.json())
        elif response.status_code == HTTPStatus.NOT_FOUND:
            raise DeviceError(response.json()['errors'][0]['title'])
        else:
            response.raise_for_status()

    @exponential_backoff(retries=5, backoff_factor=2)
    def assign_unassign_device_to_mdm_server(
        self,
        device_ids: List[str],
        server_id: Optional[str],
        action: OrgDeviceActivityType,
        access_token: str,
        mdm_migration_deadline_date_time: Optional[str] = None,
    ) -> OrgDeviceActivityResponse:
        """
        Create an org device activity for assignment, unassignment, migration deadline updates,
        migration cancellation, or device release.

        :param device_ids: List of device IDs.
        :param server_id: The ID of the MDM server for assign/unassign flows. Required for
            ASSIGN_DEVICES, UNASSIGN_DEVICES, and ASSIGN_DEVICES_WITH_MDM_MIGRATION_DEADLINE.
            Omit for UPDATE_MDM_MIGRATION_DEADLINE, CANCEL_MDM_MIGRATION, and RELEASE_DEVICES.
        :param action: Apple org device activity type.
        :param access_token: The access token for authentication.
        :param mdm_migration_deadline_date_time: ISO 8601 date-time string (e.g.,
            "2026-03-15T17:00:00.000Z") for migration workflows. Cannot be more than
            90 days in the future.
        """
        url = f'https://api-business.apple.com/v1/orgDeviceActivities'

        devices_data = [
            {
                "id": did,
                "type": "orgDevices"
            }
            for did in device_ids
        ]

        attributes = {"activityType": action}
        if mdm_migration_deadline_date_time is not None:
            attributes["activityTypeMetadata"] = {
                "mdmMigrationDeadlineDateTime": mdm_migration_deadline_date_time
            }

        relationships = {
            "devices": {
                "data": devices_data
            }
        }

        if action in {"ASSIGN_DEVICES", "UNASSIGN_DEVICES", "ASSIGN_DEVICES_WITH_MDM_MIGRATION_DEADLINE"}:
            if not server_id:
                raise ValueError(f"server_id is required for activity type {action}")
            relationships["mdmServer"] = {
                "data": {
                    "id": server_id,
                    "type": "mdmServers"
                }
            }

        if action in {"ASSIGN_DEVICES_WITH_MDM_MIGRATION_DEADLINE", "UPDATE_MDM_MIGRATION_DEADLINE"} and not mdm_migration_deadline_date_time:
            raise ValueError(f"mdm_migration_deadline_date_time is required for activity type {action}")

        request_data = {
            "data": {
                "type": "orgDeviceActivities",
                "attributes": attributes,
                "relationships": relationships,
            }
        }

        request_data = OrgDeviceActivityCreateRequest.model_validate(request_data)

        response = self.session.post(
            url,
            headers=self._auth_headers(access_token),
            json=request_data.model_dump(mode="json", exclude_none=True)
        )

        if response.status_code == HTTPStatus.CREATED:
            return OrgDeviceActivityResponse.model_validate(response.json())
        else:
            response.raise_for_status()

    @exponential_backoff(retries=5, backoff_factor=2)
    def get_device_activity(self, activity_id: str, access_token: str) -> OrgDeviceActivityResponse:
        """
        Get the status of a device activity by its ID.

        :param activity_id: The ID of the device activity.
        :param access_token: The access token for authentication.
        :return: An OrgDeviceActivityResponse object containing the activity information.
        """
        url = f'https://api-business.apple.com/v1/orgDeviceActivities/{activity_id}'
        response = self.session.get(url, headers=self._auth_headers(access_token))

        if response.status_code == HTTPStatus.OK:
            return OrgDeviceActivityResponse.model_validate(response.json())
        else:
            response.raise_for_status()
    
    @exponential_backoff(retries=5, backoff_factor=2)
    def get_apple_care_coverage(self, device_id: str, access_token: str, fields: list = None) -> AppleCareCoverageResponse:
        """
        Get AppleCare coverage information for a specific device.
        
        :param device_id: The ID of the device (serial number).
        :param access_token: The access token for authentication.
        :param fields: Optional list of fields to return, e.g., ['status', 'startDateTime', 'endDateTime']
        :return: An AppleCareCoverageResponse object containing the coverage information.
        """
        url = f'https://api-business.apple.com/v1/orgDevices/{device_id}/appleCareCoverage'
        
        # Add fields parameter if specified
        params = {}
        if fields:
            params['fields[appleCareCoverage]'] = ','.join(fields)
        
        response = self.session.get(
            url, 
            headers=self._auth_headers(access_token),
            params=params
        )
        
        if response.status_code == HTTPStatus.OK:
            return AppleCareCoverageResponse.model_validate(response.json())
        elif response.status_code == HTTPStatus.NOT_FOUND:
            raise DeviceError(response.json()['errors'][0]['title'])
        else:
            response.raise_for_status()

    @exponential_backoff(retries=5, backoff_factor=2)
    def list_users(
        self,
        access_token: str,
        limit: Optional[int] = None,
        fields: Optional[List[str]] = None,
        next: Optional[str] = None,
    ) -> UsersResponse:
        """
        Get a list of users in an organization.

        :param access_token: The access token for authentication.
        :param limit: The number of resources to return. Maximum: 1000.
        :param fields: Specific fields to return, e.g., ['firstName', 'lastName'].
        :param next: Optional; the URL for the next page of results.
        :return: A UsersResponse object containing the list of users.
        """
        if next:
            url = next
        else:
            url = 'https://api-business.apple.com/v1/users'

        params = {}
        if limit:
            params['limit'] = limit
        if fields:
            params['fields[users]'] = ','.join(fields)

        response = self.session.get(
            url,
            headers=self._auth_headers(access_token),
            params=None if next else params
        )

        if response.status_code == HTTPStatus.OK:
            return UsersResponse.model_validate(response.json())
        else:
            response.raise_for_status()

    @exponential_backoff(retries=5, backoff_factor=2)
    def get_user(
        self,
        user_id: str,
        access_token: str,
        fields: Optional[List[str]] = None,
    ) -> UserResponse:
        """
        Get information about a specific user.

        :param user_id: The unique identifier for the user.
        :param access_token: The access token for authentication.
        :param fields: Specific fields to return, e.g., ['firstName', 'lastName'].
        :return: A UserResponse object containing the user information.
        """
        url = f'https://api-business.apple.com/v1/users/{user_id}'

        params = {}
        if fields:
            params['fields[users]'] = ','.join(fields)

        response = self.session.get(
            url,
            headers=self._auth_headers(access_token),
            params=params
        )

        if response.status_code == HTTPStatus.OK:
            return UserResponse.model_validate(response.json())
        elif response.status_code == HTTPStatus.NOT_FOUND:
            raise UserError(response.json()['errors'][0]['title'])
        else:
            response.raise_for_status()
