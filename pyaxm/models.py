from pydantic import BaseModel, ConfigDict, AnyHttpUrl, AwareDatetime
from typing import List, Optional
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
    self: Optional[AnyHttpUrl]

class RelationshipLinks(BaseModel):
    include: Optional[str] = None # is this really a field? #### TODO: confirm
    related: Optional[AnyHttpUrl] = None
    self: Optional[AnyHttpUrl]

class PagedDocumentLinks(BaseModel):
    first: Optional[AnyHttpUrl] = None
    next: Optional[AnyHttpUrl] = None
    self: AnyHttpUrl

# OrgDevice
class OrgDevice(BaseModel):
    class Attributes(BaseModel):
        addedToOrgDateTime: Optional[AwareDatetime]
        color: Optional[str]
        deviceCapacity: Optional[str]
        deviceModel: Optional[str]
        eid: Optional[str]
        imei: Optional[List[str]]
        meid: Optional[List[str]]
        orderDateTime: Optional[AwareDatetime]
        orderNumber: Optional[str]
        partNumber: Optional[str]
        productFamily: Optional[str]
        productType: Optional[str]
        purchaseSourceType: Optional[str]
        purchaseSourceId: Optional[str]
        serialNumber: Optional[str]
        status: Optional[str]
        updatedDateTime: Optional[AwareDatetime]
    
    class Relationships(BaseModel):
        class AssignedServer(BaseModel):
            links: Optional[RelationshipLinks]

        assignedServer: Optional[AssignedServer]

    attributes: Optional[Attributes]
    id: str
    links: Optional[ResourceLinks]
    relationships: Optional[Relationships]
    type: str

class OrgDeviceAssignedServerLinkageResponse(BaseModel):
    class Data(BaseModel):
        id: str
        type: str

    data: Data
    links: DocumentLinks

class OrgDeviceActivity(BaseModel):
    class Attributes(BaseModel):
        createdDateTime: Optional[AwareDatetime]
        status: Optional[str]
        subStatus: Optional[str]
        completedDateTime: Optional[AwareDatetime]
        downloadUrl: Optional[str]

    attributes: Optional[Attributes]
    id: str
    links: Optional[ResourceLinks]
    type: str

class OrgDeviceActivityCreateRequest(BaseModel):
    class Data(BaseModel):
        class Attributes(BaseModel):
            activityType: OrgDeviceActivityType
            model_config = ConfigDict(use_enum_values=True)
        
        class Relationships(BaseModel):
            class Devices(BaseModel):
                class Data(BaseModel):
                    id: str
                    type: str
                
                data: List[Data]
            
            class MdmServer(BaseModel):
                class Data(BaseModel):
                    id: str
                    type: str

                data: Data

            devices: Devices
            mdmServer: MdmServer

        attributes: Attributes
        relationships: Relationships
        type: str
    data: Data

class PagingInformation(BaseModel):
    class Paging(BaseModel):
        limit: int
        nextCursor: Optional[str] = None # also weird not being passed
        total: Optional[int] = None # also not being passed

    paging: Paging

class MdmServer(BaseModel):
    class Attributes(BaseModel):
        createdDateTime: Optional[AwareDatetime]
        serverName: Optional[str]
        serverType: Optional[str]
        updatedDateTime: Optional[AwareDatetime]
    
    class Relationships(BaseModel):
        class Devices(BaseModel):
            class Data(BaseModel):
                id: str
                type: str

            data: Optional[List[Data]] = None # weird also not being returned
            links: Optional[RelationshipLinks]
            meta: Optional[PagingInformation] = None # also weird

        devices: Optional[Devices]

    attributes: Optional[Attributes]
    id: str
    relationships: Optional[Relationships]
    type: str

class MdmServerLinkageResponse(BaseModel):
    class Data(BaseModel):
        id: str
        type: str

    data: Data
    links: PagedDocumentLinks
    meta: Optional[PagingInformation]

class OrgDeviceActivityResponse(BaseModel):
    data: OrgDeviceActivity
    links: DocumentLinks

class MdmServersResponse(BaseModel):
    data: List[MdmServer]
    included: Optional[List[OrgDevice]] = None # weird not being returned
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
            source: Optional[str]
        
        href: Optional[AnyHttpUrl]
        meta: Optional[Meta]
    
    about: Optional[AnyHttpUrl]
    associated: Optional[AnyHttpUrl|Associated]

class ErrorResponse(BaseModel):
    class Errors(BaseModel):
        class Meta(BaseModel):
            # allows non-specified key/value pairs
            model_config = ConfigDict(extra='allow')

        code: str
        detail: str
        id: Optional[str]
        source: Optional[JsonPointer|Parameter] = None
        status: str
        title: str
        links: Optional[ErrorLinks] = None
        meta: Optional[Meta] = None
    
    errors: Optional[List[Errors]]

class MdmServerDevicesLinkagesResponse(BaseModel):
    class Data(BaseModel):
        id: str
        type: str

    data: List[Data]
    links: PagedDocumentLinks
    meta: Optional[PagingInformation]
