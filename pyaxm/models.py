from pydantic import BaseModel, ConfigDict, AnyHttpUrl, AwareDatetime
from typing import List, Optional, Literal
from enum import Enum

class OrgDeviceActivityType(Enum):
    ASSIGN_DEVICES = "ASSIGN_DEVICES"
    UNASSIGN_DEVICES = "UNASSIGN_DEVICES"

class DocumentLinks(BaseModel):
    self: AnyHttpUrl

class Parameter(BaseModel):
    parameter: str

class JsonPointer(BaseModel):
    pointer: str

class ResourceLinks(BaseModel):
    self: Optional[AnyHttpUrl] = None

class RelationshipLinks(BaseModel):
    include: Optional[AnyHttpUrl] = None
    related: Optional[AnyHttpUrl] = None
    self: Optional[AnyHttpUrl] = None

class PagedDocumentLinks(BaseModel):
    first: Optional[AnyHttpUrl] = None
    next: Optional[AnyHttpUrl] = None
    self: AnyHttpUrl

# OrgDevice
class OrgDevice(BaseModel):
    class Attributes(BaseModel):
        addedToOrgDateTime: Optional[AwareDatetime] = None
        color: Optional[str] = None
        deviceCapacity: Optional[str] = None
        deviceModel: Optional[str] = None
        eid: Optional[str] = None
        imei: Optional[List[str]] = None
        meid: Optional[List[str]] = None
        wifiMacAddress: Optional[str] = None
        bluetoothMacAddress: Optional[str] = None
        orderDateTime: Optional[AwareDatetime] = None
        orderNumber: Optional[str] = None
        partNumber: Optional[str] = None
        productFamily: Optional[str] = None
        productType: Optional[str] = None
        purchaseSourceType: Optional[str] = None
        purchaseSourceId: Optional[str] = None
        serialNumber: Optional[str] = None
        status: Optional[str] = None
        updatedDateTime: Optional[AwareDatetime] = None
    
    class Relationships(BaseModel):
        class AssignedServer(BaseModel):
            links: Optional[RelationshipLinks]

        assignedServer: Optional[AssignedServer]

    attributes: Optional[Attributes]
    id: str
    links: Optional[ResourceLinks]
    relationships: Optional[Relationships]
    type: Literal['orgDevices']

class OrgDeviceAssignedServerLinkageResponse(BaseModel):
    class Data(BaseModel):
        id: str
        type: Literal['mdmServers']

    data: Data
    links: DocumentLinks

class OrgDeviceActivity(BaseModel):
    class Attributes(BaseModel):
        createdDateTime: Optional[AwareDatetime] = None
        status: Optional[str] = None
        subStatus: Optional[str] = None
        completedDateTime: Optional[AwareDatetime] = None
        downloadUrl: Optional[str] = None

    attributes: Optional[Attributes]
    id: str
    links: Optional[ResourceLinks]
    type: Literal['orgDeviceActivities']

class OrgDeviceActivityCreateRequest(BaseModel):
    class Data(BaseModel):
        class Attributes(BaseModel):
            activityType: OrgDeviceActivityType
            model_config = ConfigDict(use_enum_values=True)
        
        class Relationships(BaseModel):
            class Devices(BaseModel):
                class Data(BaseModel):
                    id: str
                    type: Literal['orgDevices']
                
                data: List[Data]
            
            class MdmServer(BaseModel):
                class Data(BaseModel):
                    id: str
                    type: Literal['mdmServers']

                data: Data

            devices: Devices
            mdmServer: MdmServer

        attributes: Attributes
        relationships: Relationships
        type: Literal['orgDeviceActivities']
    data: Data

class PagingInformation(BaseModel):
    class Paging(BaseModel):
        limit: int
        nextCursor: Optional[str] = None
        total: Optional[int] = None

    paging: Paging

class MdmServer(BaseModel):
    class Attributes(BaseModel):
        createdDateTime: Optional[AwareDatetime] = None
        serverName: Optional[str] = None
        serverType: Optional[str] = None
        updatedDateTime: Optional[AwareDatetime] = None
    
    class Relationships(BaseModel):
        class Devices(BaseModel):
            class Data(BaseModel):
                id: str
                type: Literal['orgDevices']

            data: Optional[List[Data]] = None
            links: Optional[RelationshipLinks]
            meta: Optional[PagingInformation] = None

        devices: Optional[Devices]

    attributes: Optional[Attributes]
    id: str
    relationships: Optional[Relationships]
    type: Literal['mdmServers']

class OrgDeviceActivityResponse(BaseModel):
    data: OrgDeviceActivity
    links: DocumentLinks

class MdmServersResponse(BaseModel):
    data: List[MdmServer]
    included: Optional[List[OrgDevice]] = None
    links: PagedDocumentLinks
    meta: Optional[PagingInformation]

class MdmServerResponse(BaseModel):
    data: MdmServer
    included: Optional[List[OrgDevice]]
    links: DocumentLinks

class OrgDevicesResponse(BaseModel):
    data: List[OrgDevice]
    links: PagedDocumentLinks
    meta: Optional[PagingInformation]

class OrgDeviceResponse(BaseModel):
    data: OrgDevice
    links: DocumentLinks

class ErrorLinks(BaseModel):
    class Associated(BaseModel):
        class Meta(BaseModel):
            source: Optional[str] = None
        
        href: Optional[AnyHttpUrl] = None
        meta: Optional[Meta] = None
    
    about: Optional[AnyHttpUrl] = None
    associated: Optional[AnyHttpUrl|Associated] = None

class ErrorResponse(BaseModel):
    class Errors(BaseModel):
        class Meta(BaseModel):
            # allows non-specified key/value pairs
            model_config = ConfigDict(extra='allow')

        code: str
        detail: str
        id: Optional[str] = None
        source: Optional[JsonPointer|Parameter] = None
        status: str
        title: str
        links: Optional[ErrorLinks] = None
        meta: Optional[Meta] = None
    
    errors: Optional[List[Errors]]

class MdmServerDevicesLinkagesResponse(BaseModel):
    class Data(BaseModel):
        id: str
        type: Literal['orgDevices']

    data: List[Data]
    links: PagedDocumentLinks
    meta: Optional[PagingInformation]
