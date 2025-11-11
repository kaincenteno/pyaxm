from pydantic import BaseModel, ConfigDict, AnyHttpUrl, AwareDatetime
from typing import List, Optional, Literal
from enum import Enum

class OrgDeviceActivityType(Enum):
    ASSIGN_DEVICES = "ASSIGN_DEVICES"
    UNASSIGN_DEVICES = "UNASSIGN_DEVICES"

class AppleCareCoverageStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class AppleCareCoveragePaymentType(str, Enum):
    ABE_SUBSCRIPTION = "ABE_SUBSCRIPTION"
    PAID_UP_FRONT = "PAID_UP_FRONT"
    SUBSCRIPTION = "SUBSCRIPTION"
    NONE = "NONE"

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
        releasedFromOrgDateTime: Optional[AwareDatetime] = None
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
            links: Optional[RelationshipLinks] = None
        
        class AppleCareCoverage(BaseModel):
            links: Optional[RelationshipLinks] = None

        assignedServer: Optional[AssignedServer] = None
        appleCareCoverage: Optional[AppleCareCoverage] = None

    attributes: Optional[Attributes] = None
    id: str
    links: Optional[ResourceLinks] = None
    relationships: Optional[Relationships] = None
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

    attributes: Optional[Attributes] = None
    id: str
    links: Optional[ResourceLinks] = None
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
            links: Optional[RelationshipLinks] = None
            meta: Optional[PagingInformation] = None

        devices: Optional[Devices] = None

    attributes: Optional[Attributes] = None
    id: str
    relationships: Optional[Relationships] = None
    type: Literal['mdmServers']

class OrgDeviceActivityResponse(BaseModel):
    data: OrgDeviceActivity
    links: DocumentLinks

class MdmServersResponse(BaseModel):
    data: List[MdmServer]
    included: Optional[List[OrgDevice]] = None
    links: PagedDocumentLinks
    meta: Optional[PagingInformation] = None

class MdmServerResponse(BaseModel):
    data: MdmServer
    included: Optional[List[OrgDevice]] = None
    links: DocumentLinks

class OrgDevicesResponse(BaseModel):
    data: List[OrgDevice]
    links: PagedDocumentLinks
    meta: Optional[PagingInformation] = None

class OrgDeviceResponse(BaseModel):
    data: OrgDevice
    links: DocumentLinks
    meta: Optional[PagingInformation] = None

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
    
    errors: Optional[List[Errors]] = None

class MdmServerDevicesLinkagesResponse(BaseModel):
    class Data(BaseModel):
        id: str
        type: Literal['orgDevices']

    data: List[Data]
    links: PagedDocumentLinks
    meta: Optional[PagingInformation] = None

class AppleCareCoverage(BaseModel):
    class Attributes(BaseModel):
        status: Optional[AppleCareCoverageStatus] = None
        paymentType: Optional[AppleCareCoveragePaymentType] = None
        description: Optional[str] = None
        startDateTime: Optional[AwareDatetime] = None
        endDateTime: Optional[AwareDatetime] = None
        isRenewable: Optional[bool] = None
        isCanceled: Optional[bool] = None
        contractCancelDateTime: Optional[AwareDatetime] = None
        agreementNumber: Optional[str] = None

    attributes: Optional[Attributes] = None
    id: str
    type: Literal['appleCareCoverage']
    model_config = ConfigDict(use_enum_values=True)

class AppleCareCoverageResponse(BaseModel):
    data: List[AppleCareCoverage]
    links: DocumentLinks
    meta: Optional[PagingInformation] = None
