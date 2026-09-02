import os
import time

from pyaxm.abm_requests import ABMRequests
from pyaxm.auth import TokenManager
from pyaxm.models import (
    OrgDevice,
    AppleCareCoverage,
    MdmServer,
    MdmServerDevicesLinkagesResponse,
    OrgDeviceAssignedServerLinkageResponse,
    OrgDeviceActivity,
    OrgDeviceActivityType,
    AuditEvent,
    User,
)
from typing import List, Optional

class Client:
    def __init__(self, axm_client_id=None, axm_key_id=None, key_path=None, token_path=None):
        ABM_FOLDER = os.path.join(os.path.expanduser('~'), '.config', 'pyaxm')
        axm_client_id = axm_client_id or os.environ.get('AXM_CLIENT_ID')
        axm_key_id = axm_key_id or os.environ.get('AXM_KEY_ID')
        key_path = key_path or os.path.join(ABM_FOLDER, 'key.pem')
        token_path = token_path or os.path.join(ABM_FOLDER, 'token.json')

        self.abm = ABMRequests()
        self.token_manager = TokenManager(
            abm_requests=self.abm,
            axm_client_id=axm_client_id,
            axm_key_id=axm_key_id,
            key_path=key_path,
            token_path=token_path,
        )

    def list_devices(self) -> list[OrgDevice]:
        response = self.abm.list_devices(self.token_manager.get_token_value())
        devices = response.data
        
        while response.links.next:
            next_page = response.links.next
            response = self.abm.list_devices(self.token_manager.get_token_value(), next=next_page)
            devices.extend(response.data)
        
        return devices

    def get_device(self, device_id: str) -> OrgDevice:
        response = self.abm.get_device(device_id, self.token_manager.get_token_value())
        return response.data

    def get_apple_care_coverage(self, device_id: str) -> list[AppleCareCoverage]:
        response = self.abm.get_apple_care_coverage(device_id, self.token_manager.get_token_value())
        return response.data

    def list_mdm_servers(self) -> list[MdmServer]:
        response = self.abm.list_mdm_servers(self.token_manager.get_token_value())
        return response.data

    def get_audit_events(
        self,
        start_timestamp: str,
        end_timestamp: str,
        actor_id: Optional[str] = None,
        subject_id: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: Optional[int] = None,
        fields: Optional[List[str]] = None,
        cursor: Optional[str] = None,
    ) -> List[AuditEvent]:
        response = self.abm.get_audit_events(
            self.token_manager.get_token_value(),
            start_timestamp,
            end_timestamp,
            actor_id,
            subject_id,
            event_type,
            limit,
            fields,
            cursor
        )
        events = response.data
        
        while response.links.next:
            next_page = response.links.next
            response = self.abm.get_audit_events(
                self.token_manager.get_token_value(),
                start_timestamp,
                end_timestamp,
                next=next_page
            )
            events.extend(response.data)

        return events

    def list_devices_in_mdm_server(self, server_id: str) -> list[MdmServerDevicesLinkagesResponse.Data]:
        response = self.abm.list_devices_in_mdm_server(server_id, self.token_manager.get_token_value())
        devices = response.data
        while response.links.next:
            next_page = response.links.next
            response = self.abm.list_devices_in_mdm_server(server_id, self.token_manager.get_token_value(), next=next_page)
            devices.extend(response.data)
        return devices

    def get_device_server_assignment(self, device_id: str) -> OrgDeviceAssignedServerLinkageResponse.Data:
        response = self.abm.get_device_server_assignment(device_id, self.token_manager.get_token_value())
        return response.data

    def _wait_for_device_activity_completion(
        self,
        activity_id: str,
        backoff_factor: int = 2,
        max_retries: int = 5,
    ) -> OrgDeviceActivity:
        activity_response = self.abm.get_device_activity(activity_id, self.token_manager.get_token_value())
        retry = 0
        while activity_response.data.attributes.status == 'IN_PROGRESS' and retry < max_retries:
            time.sleep(backoff_factor ** (retry + 1))
            retry += 1
            activity_response = self.abm.get_device_activity(activity_id, self.token_manager.get_token_value())
        return activity_response.data

    def assign_unassign_device_to_mdm_server(
        self,
        device_ids: List[str],
        server_id: Optional[str],
        action: OrgDeviceActivityType,
        mdm_migration_deadline_date_time: Optional[str] = None,
    ) -> OrgDeviceActivity:
        response = self.abm.assign_unassign_device_to_mdm_server(
            device_ids,
            server_id,
            action,
            self.token_manager.get_token_value(),
            mdm_migration_deadline_date_time,
        )
        return self._wait_for_device_activity_completion(response.data.id)

    def list_users(self) -> List[User]:
        response = self.abm.list_users(self.token_manager.get_token_value())
        users = response.data

        while response.links.next:
            next_page = response.links.next
            response = self.abm.list_users(self.token_manager.get_token_value(), next=next_page)
            users.extend(response.data)

        return users

    def get_user(self, user_id: str) -> User:
        response = self.abm.get_user(user_id, self.token_manager.get_token_value())
        return response.data
