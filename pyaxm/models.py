from pydantic import BaseModel, ConfigDict, AnyHttpUrl, AwareDatetime, Field
from typing import Annotated, List, Optional, Literal, TypeAlias, Union

OrgDeviceActivityType: TypeAlias = str
AppleCareCoverageStatus: TypeAlias = str
AppleCareCoveragePaymentType: TypeAlias = str
MdmServerStatus: TypeAlias = str
MdmServerProductFamily: TypeAlias = str
UserStatus: TypeAlias = str
UserPhoneNumberType: TypeAlias = str

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
        ethernetMacAddress: Optional[List[str]] = None
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
        # releaserEntityType: Optional[str] = None Documented, but not returned
        # releaserId: Optional[str] = None Documented but not returned
    
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
        defaultProductFamilies: Optional[List[MdmServerProductFamily]] = None
        deviceCount: Optional[int] = None
        enableMdmDisownFlag: Optional[bool] = None
        lastConnectedDateTime: Optional[AwareDatetime] = None
        lastConnectedIp: Optional[str] = None
        serverName: Optional[str] = None
        serverType: Optional[str] = None
        status: Optional[MdmServerStatus] = None
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

class AppleCareCoverageResponse(BaseModel):
    data: List[AppleCareCoverage]
    links: DocumentLinks
    meta: Optional[PagingInformation] = None

class AuditEventCommonAttributes(BaseModel):
    eventDateTime: Optional[AwareDatetime] = None
    type: str
    category: Optional[str] = None
    actorType: Optional[str] = None
    actorId: Optional[str] = None
    actorName: Optional[str] = None
    subjectType: Optional[str] = None
    subjectId: Optional[str] = None
    subjectName: Optional[str] = None
    outcome: Optional[str] = None
    groupId: Optional[str] = None

# Audit event inner data objects

class AuditEventAccountRoleLocation(BaseModel):
    roleName: Optional[str] = None
    locationUniqueIdentifier: Optional[str] = None

class AuditEventAccountAdded(BaseModel):
    pass

class AuditEventAccountDeleted(BaseModel):
    pass

class AuditEventAccountRoleLocationChanged(BaseModel):
    accountRoleLocationList: Optional[List[AuditEventAccountRoleLocation]] = None

class AuditEventApiAccountCreatedWithKey(BaseModel):
    keyId: Optional[str] = None

class AuditEventApiAccountCreatedWithoutKey(BaseModel):
    pass

class AuditEventApiAccountDeleted(BaseModel):
    pass

class AuditEventApiAccountKeyGenerated(BaseModel):
    keyId: Optional[str] = None

class AuditEventApiAccountKeyRevoked(BaseModel):
    keyId: Optional[str] = None

class AuditEventApiAccountNameChanged(BaseModel):
    newName: Optional[str] = None

class AuditEventApiAccountRoleLocationChanged(BaseModel):
    apiAccountRoleLocationList: Optional[List[AuditEventAccountRoleLocation]] = None

class AuditEventCollectionCreated(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class AuditEventCollectionDeleted(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class AuditEventCollectionUpdated(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class AuditEventConfigSettingsCreated(BaseModel):
    configType: Optional[str] = None
    configId: Optional[str] = None
    configVersion: Optional[str] = None

class AuditEventConfigSettingsDeleted(BaseModel):
    configType: Optional[str] = None
    configId: Optional[str] = None
    configVersion: Optional[str] = None

class AuditEventConfigSettingsUpdated(BaseModel):
    configType: Optional[str] = None
    configId: Optional[str] = None
    configVersion: Optional[str] = None

class AuditEventDeviceAddedToOrg(BaseModel):
    serialNumber: Optional[str] = None
    purchaseSourceType: Optional[str] = None
    purchaseSourceId: Optional[str] = None

class AuditEventDeviceAssignedToServer(BaseModel):
    serialNumber: Optional[str] = None
    targetServerName: Optional[str] = None

class AuditEventDeviceIsErased(BaseModel):
    pass

class AuditEventDeviceRemovedFromOrg(BaseModel):
    serialNumber: Optional[str] = None
    releaseEntityId: Optional[str] = None
    releaseEntityType: Optional[str] = None

class AuditEventDeviceUnassignedFromServer(BaseModel):
    serialNumber: Optional[str] = None

class AuditEventDomainAdded(BaseModel):
    pass

class AuditEventDomainRemoved(BaseModel):
    pass

class AuditEventDomainVerified(BaseModel):
    pass

class AuditEventExternalAccountAssociated(BaseModel):
    pass

class AuditEventExternalAccountDisassociated(BaseModel):
    pass

class AuditEventSubjectHasAppleCarePurchaseAdded(BaseModel):
    subscriptionId: Optional[str] = None

class AuditEventSubjectHasAppleCarePurchaseRemoved(BaseModel):
    subscriptionId: Optional[str] = None

class AuditEventSubjectHasICloudStoragePurchaseAdded(BaseModel):
    subscriptionId: Optional[str] = None

class AuditEventSubjectHasICloudStoragePurchaseRemoved(BaseModel):
    subscriptionId: Optional[str] = None

class AuditEventSubscriptionCreated(BaseModel):
    planCaption: Optional[str] = None

class AuditEventSubscriptionDeleted(BaseModel):
    planCaption: Optional[str] = None

class AuditEventSubscriptionUpdated(BaseModel):
    planCaption: Optional[str] = None

# AuditEvent *Attributes - Inherited from AuditEventCommonAttributes

class AuditEventAccountAddedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataAccountAdded']
    eventDataAccountAdded: Optional[AuditEventAccountAdded] = None

class AuditEventAccountDeletedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataAccountDeleted']
    eventDataAccountDeleted: Optional[AuditEventAccountDeleted] = None

class AuditEventAccountRoleLocationChangedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataAccountRoleLocationChanged']
    eventDataAccountRoleLocationChanged: Optional[AuditEventAccountRoleLocationChanged] = None

class AuditEventApiAccountCreatedWithKeyAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataApiAccountCreatedWithKey']
    eventDataApiAccountCreatedWithKey: Optional[AuditEventApiAccountCreatedWithKey] = None

class AuditEventApiAccountCreatedWithoutKeyAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataApiAccountCreatedWithoutKey']
    eventDataApiAccountCreatedWithoutKey: Optional[AuditEventApiAccountCreatedWithoutKey] = None

class AuditEventApiAccountDeletedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataApiAccountDeleted']
    eventDataApiAccountDeleted: Optional[AuditEventApiAccountDeleted] = None

class AuditEventApiAccountKeyGeneratedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataApiAccountKeyGenerated']
    eventDataApiAccountKeyGenerated: Optional[AuditEventApiAccountKeyGenerated] = None

class AuditEventApiAccountKeyRevokedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataApiAccountKeyRevoked']
    eventDataApiAccountKeyRevoked: Optional[AuditEventApiAccountKeyRevoked] = None

class AuditEventApiAccountNameChangedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataApiAccountNameChanged']
    eventDataApiAccountNameChanged: Optional[AuditEventApiAccountNameChanged] = None

class AuditEventApiAccountRoleLocationChangedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataApiAccountRoleLocationChanged']
    eventDataApiAccountRoleLocationChanged: Optional[AuditEventApiAccountRoleLocationChanged] = None

class AuditEventCollectionCreatedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataCollectionCreated']
    eventDataCollectionCreated: Optional[AuditEventCollectionCreated] = None

class AuditEventCollectionDeletedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataCollectionDeleted']
    eventDataCollectionDeleted: Optional[AuditEventCollectionDeleted] = None

class AuditEventCollectionUpdatedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataCollectionUpdated']
    eventDataCollectionUpdated: Optional[AuditEventCollectionUpdated] = None

class AuditEventConfigSettingsCreatedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataConfigSettingsCreated']
    eventDataConfigSettingsCreated: Optional[AuditEventConfigSettingsCreated] = None

class AuditEventConfigSettingsDeletedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataConfigSettingsDeleted']
    eventDataConfigSettingsDeleted: Optional[AuditEventConfigSettingsDeleted] = None

class AuditEventConfigSettingsUpdatedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataConfigSettingsUpdated']
    eventDataConfigSettingsUpdated: Optional[AuditEventConfigSettingsUpdated] = None

class AuditEventDeviceAddedToOrgAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataDeviceAddedToOrg']
    eventDataDeviceAddedToOrg: Optional[AuditEventDeviceAddedToOrg] = None

class AuditEventDeviceAssignedToServerAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataDeviceAssignedToServer']
    eventDataDeviceAssignedToServer: Optional[AuditEventDeviceAssignedToServer] = None

class AuditEventDeviceIsErasedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataDeviceIsErased']
    eventDataDeviceIsErased: Optional[AuditEventDeviceIsErased] = None

class AuditEventDeviceRemovedFromOrgAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataDeviceRemovedFromOrg']
    eventDataDeviceRemovedFromOrg: Optional[AuditEventDeviceRemovedFromOrg] = None

class AuditEventDeviceUnassignedFromServerAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataDeviceUnassignedFromServer']
    eventDataDeviceUnassignedFromServer: Optional[AuditEventDeviceUnassignedFromServer] = None

class AuditEventDomainAddedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataDomainAdded']
    eventDataDomainAdded: Optional[AuditEventDomainAdded] = None

class AuditEventDomainRemovedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataDomainRemoved']
    eventDataDomainRemoved: Optional[AuditEventDomainRemoved] = None

class AuditEventDomainVerifiedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataDomainVerified']
    eventDataDomainVerified: Optional[AuditEventDomainVerified] = None

class AuditEventExternalAccountAssociatedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataExternalAccountAssociated']
    eventDataExternalAccountAssociated: Optional[AuditEventExternalAccountAssociated] = None

class AuditEventExternalAccountDisassociatedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataExternalAccountDisassociated']
    eventDataExternalAccountDisassociated: Optional[AuditEventExternalAccountDisassociated] = None

class AuditEventSubjectHasAppleCarePurchaseAddedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataSubjectHasAppleCarePurchaseAdded']
    eventDataSubjectHasAppleCarePurchaseAdded: Optional[AuditEventSubjectHasAppleCarePurchaseAdded] = None

class AuditEventSubjectHasAppleCarePurchaseRemovedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataSubjectHasAppleCarePurchaseRemoved']
    eventDataSubjectHasAppleCarePurchaseRemoved: Optional[AuditEventSubjectHasAppleCarePurchaseRemoved] = None

class AuditEventSubjectHasICloudStoragePurchaseAddedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataSubjectHasICloudStoragePurchaseAdded']
    eventDataSubjectHasICloudStoragePurchaseAdded: Optional[AuditEventSubjectHasICloudStoragePurchaseAdded] = None

class AuditEventSubjectHasICloudStoragePurchaseRemovedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataSubjectHasICloudStoragePurchaseRemoved']
    eventDataSubjectHasICloudStoragePurchaseRemoved: Optional[AuditEventSubjectHasICloudStoragePurchaseRemoved] = None

class AuditEventSubscriptionCreatedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataSubscriptionCreated']
    eventDataSubscriptionCreated: Optional[AuditEventSubscriptionCreated] = None

class AuditEventSubscriptionDeletedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataSubscriptionDeleted']
    eventDataSubscriptionDeleted: Optional[AuditEventSubscriptionDeleted] = None

class AuditEventSubscriptionUpdatedAttributes(AuditEventCommonAttributes):
    eventDataPropertyKey: Literal['eventDataSubscriptionUpdated']
    eventDataSubscriptionUpdated: Optional[AuditEventSubscriptionUpdated] = None


AuditEventAttributes = Annotated[
    Union[
        AuditEventAccountAddedAttributes,
        AuditEventAccountDeletedAttributes,
        AuditEventAccountRoleLocationChangedAttributes,
        AuditEventApiAccountCreatedWithKeyAttributes,
        AuditEventApiAccountCreatedWithoutKeyAttributes,
        AuditEventApiAccountDeletedAttributes,
        AuditEventApiAccountKeyGeneratedAttributes,
        AuditEventApiAccountKeyRevokedAttributes,
        AuditEventApiAccountNameChangedAttributes,
        AuditEventApiAccountRoleLocationChangedAttributes,
        AuditEventCollectionCreatedAttributes,
        AuditEventCollectionDeletedAttributes,
        AuditEventCollectionUpdatedAttributes,
        AuditEventConfigSettingsCreatedAttributes,
        AuditEventConfigSettingsDeletedAttributes,
        AuditEventConfigSettingsUpdatedAttributes,
        AuditEventDeviceAddedToOrgAttributes,
        AuditEventDeviceAssignedToServerAttributes,
        AuditEventDeviceIsErasedAttributes,
        AuditEventDeviceRemovedFromOrgAttributes,
        AuditEventDeviceUnassignedFromServerAttributes,
        AuditEventDomainAddedAttributes,
        AuditEventDomainRemovedAttributes,
        AuditEventDomainVerifiedAttributes,
        AuditEventExternalAccountAssociatedAttributes,
        AuditEventExternalAccountDisassociatedAttributes,
        AuditEventSubjectHasAppleCarePurchaseAddedAttributes,
        AuditEventSubjectHasAppleCarePurchaseRemovedAttributes,
        AuditEventSubjectHasICloudStoragePurchaseAddedAttributes,
        AuditEventSubjectHasICloudStoragePurchaseRemovedAttributes,
        AuditEventSubscriptionCreatedAttributes,
        AuditEventSubscriptionDeletedAttributes,
        AuditEventSubscriptionUpdatedAttributes,
    ],
    Field(discriminator='eventDataPropertyKey')
]

class AuditEvent(BaseModel):
    attributes: Optional[AuditEventAttributes] = None
    id: str
    type: Literal['auditEvents']

class AuditEventsResponse(BaseModel):
    data: List[AuditEvent]
    links: PagedDocumentLinks
    meta: Optional[PagingInformation] = None

# User
class UserPhoneNumber(BaseModel):
    phoneNumber: Optional[str] = None
    type: Optional[UserPhoneNumberType] = None

class UserRoleOuMapping(BaseModel):
    roleName: Optional[str] = None
    ouId: Optional[str] = None

class User(BaseModel):
    class Attributes(BaseModel):
        firstName: Optional[str] = None
        middleName: Optional[str] = None
        lastName: Optional[str] = None
        status: Optional[UserStatus] = None
        managedAppleAccount: Optional[str] = None
        isExternalUser: Optional[bool] = None
        roleOuList: Optional[List[UserRoleOuMapping]] = None
        email: Optional[str] = None
        employeeNumber: Optional[str] = None
        costCenter: Optional[str] = None
        division: Optional[str] = None
        department: Optional[str] = None
        jobTitle: Optional[str] = None
        phoneNumbers: Optional[List[UserPhoneNumber]] = None
        startDateTime: Optional[AwareDatetime] = None
        createdDateTime: Optional[AwareDatetime] = None
        updatedDateTime: Optional[AwareDatetime] = None

    attributes: Optional[Attributes] = None
    id: str
    links: Optional[ResourceLinks] = None
    type: Literal['users']

class UserResponse(BaseModel):
    data: User
    links: DocumentLinks

class UsersResponse(BaseModel):
    data: List[User]
    links: PagedDocumentLinks
    meta: Optional[PagingInformation] = None
