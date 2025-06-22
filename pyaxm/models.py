from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from enum import Enum

class OrgDeviceActivityType(Enum):
    ASSIGN_DEVICES = "ASSIGN_DEVICES"
    UNASSIGN_DEVICES = "UNASSIGN_DEVICES"

class DocumentLinks(BaseModel):
    self: str # uri-reference to the current document

class Parameter(BaseModel):
    parameter: str

class JsonPointer(BaseModel):
    pointer: str

class ResourceLinks(BaseModel):
    self: Optional[str] # uri-reference. Link to the resource

class RelationshipLinks(BaseModel):
    include: Optional[str] = None # is this really a field? #### TODO: confirm
    related: Optional[str] = None # uri-reference
    self: Optional[str] # uri-reference

class PagedDocumentLinks(BaseModel):
    first: Optional[str] = None # uri-reference
    next: Optional[str] = None # uri-reference
    self: str # uri-reference

# OrgDevice
class OrgDevice(BaseModel):
    class Attributes(BaseModel):
        addedToOrgDateTime: Optional[str] # ISO 8601 date-time
        color: Optional[str]
        deviceCapacity: Optional[str]
        deviceModel: Optional[str]
        eid: Optional[str]
        imei: Optional[List[str]]
        meid: Optional[List[str]]
        orderDateTime: Optional[str] # ISO 8601 date-time
        orderNumber: Optional[str]
        partNumber: Optional[str]
        productFamily: Optional[str]
        productType: Optional[str]
        purchaseSourceType: Optional[str]
        purchaseSourceId: Optional[str]
        serialNumber: Optional[str]
        status: Optional[str]
        updatedDateTime: Optional[str] # ISO 8601 date-time
    
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
        createdDateTime: Optional[str] # ISO 8601 date-time
        status: Optional[str]
        subStatus: Optional[str]
        completedDateTime: Optional[str] # ISO 8601 date-time
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
        createdDateTime: Optional[str] # ISO 8601 date-time
        serverName: Optional[str]
        serverType: Optional[str]
        updatedDateTime: Optional[str] # ISO 8601 date-time
    
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
        
        href: Optional[str] # uri-reference
        meta: Optional[Meta]
    
    about: Optional[str] # uri-reference
    associated: Optional[str|Associated] # uri-reference or Associated object

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
