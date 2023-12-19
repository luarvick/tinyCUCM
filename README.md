<a name="readme-top"></a>

<!-- PROJECT NAME -->
<br />
<div align="center">
  <h3 align="center">tinyCUCM</h3>
  <p align="center">Cisco Unified Call Manager AXL Methods Collection.</p>
</div>

---

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#installation">Installation</a></li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#instance-create">Instance Create</a></li>
        <li><a href="#axl-collection">AXL Collection</a></li>
        <ul>
          <li><a href="#add-methods">Add Methods</a></li>
          <li><a href="#do-methods">Do Methods</a></li>
          <li><a href="#get-methods">Get Methods</a></li>
          <li><a href="#remove-methods">Remove Methods</a></li>
          <li><a href="#reset-methods">Reset Methods</a></li>
          <li><a href="#restart-methods">Restart Methods</a></li>
          <li><a href="#update-methods">Update Methods</a></li>
        </ul>
        <li><a href="#sql-collection">SQL Collection</a></li>
        <ul>
          <li><a href="#execute-query">Execute Query</a></li>
          <li><a href="#update-query">Update Query</a></li>
          <li><a href="#predefined-queries">Predefined Queries</a></li>
        </ul>
        <li><a href="#create-yor-own-methods">Create Your Own Methods</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

---

<!-- ABOUT THE PROJECT -->
## About The Project

This project is for informational purposes only and is intended to study the capabilities of the Cisco Unified Call Manager's API. 
Methods have been tested on CUCM ver. 11.5.\
[Cisco UCM AXL Schemas & SQL Data Dictionaries Documentation](https://developer.cisco.com/docs/axl/#!archived-references)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- INSTALLATION -->
## Installation

Installation is as simple as:

   ```sh
   pip install tinyCUCM
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage


### Instance Create

Download `Cisco AXL Toolkit` from the station (`Application` -> `Plugins`) and put it into the folder with your project.\
Create an Cisco UCM application account or local end user with `Standard CCM Super Users` privileges (Assing Access Control Group to `Your-CUCM-Account`).\
Create a new instance of the `CucmAxlClient` class and assigns this object to the local variable `cucm`.

<span style="color:#ff0000">**Don't store sensitive information in source code. For example use ".env" file.**</span>

<details>
<summary>Code Example:</summary>

```python
from pathlib import Path
from tinyCUCM import CucmAxlClient


BASE_DIR = Path(__file__).resolve().parent
settings = {
    "pub_fqdn": "cucm.example.com",
    "pub_version": "11.5",
    "user_login": "Your-CUCM-Account",
    "user_password": "You%wILL#&neVeR!gUEss",
    "toolkit_path": BASE_DIR / "axlsqltoolkit",
    "cert_path": BASE_DIR / "cucm.crt",
    "session_verify": False,
    "session_timeout": 15,
}

if __name__ == "__main__":
    cucm = CucmAxlClient(**settings)
    # Get All AXL Method Names
    print(cucm.axlAllMethods())

# (
#     'addAarGroup', 
#     'addAdvertisedPatterns', 
#     'addAnnouncement', 
#     'addAppServerInfo', 
#     'addAppUser', 
#     ...,
#     'updateWifiHotspot', 
#     'updateWirelessAccessPointControllers', 
#     'updateWlanProfileGroup', 
#     'wipePhone'
# )
```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### AXL Collection


#### Add Methods

<details>
<summary>Code Example:</summary>

```python

```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Do Methods

* `axlDoAuthenticateUser` -  required keys: (`userid`, `password`) or (`userid`, `pin`)
* `axlDoDeviceLogin` -  required keys: (`deviceName`, `loginDuration`, `profileName`, `userId`)\
  * Key `loginDuration: str = "0"` - Logout disabled\
  * Key `loginDuration: str = "36000"` - Logout after 10h
* `axlDoDeviceLogout` -  required keys: `deviceName`
* `axlDoLdapSync` -  required keys: (`uuid`, `sync`) or (`name`, `sync`)\
  * Key `sync: bool = True` - Start Synchronization\
  * Key `sync: bool = False` - Cancel the Synchronization which is currently under process

<details>
<summary>Code Example:</summary>

```python
cucm = ...
print("Result:", cucm.axlDoAuthenticateUser(**{"userid": "...", "password": "..."}))
# Result: {'return': {'userAuthenticated': 'true', 'code': 0, 'daysToExpiry': 0, 'isWarningNeeded': 'false'}, 'sequence': None}
# Result: {'return': {'userAuthenticated': 'false', 'code': 1, 'daysToExpiry': 0, 'isWarningNeeded': 'false'}, 'sequence': None}

print("Result:", cucm.axlDoDeviceLogin(**{"deviceName": "SEP...", "loginDuration": "...", "profileName":"...", "userid": "..."}))
# Result {'return': '{........-....-....-....-............}', 'sequence': None}

print("Result:", cucm.axlDoDeviceLogout(**{"deviceName": "SEP..."}))
# Result {'return': '{........-....-....-....-............}', 'sequence': None}

print("Result:", cucm.axlDoLdapSync(**{"uuid": "........-....-....-....-............", "sync": True}))
# Result: {'return': 'Sync initiated successfully', 'sequence': None}
```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Get Methods

* `axlGetCallPickupGroup` -  required keys: `uuid` or `name` or `pattern` or (`pattern`, `routePartitionName`)
* `axlGetDeviceProfile` -  required keys: `uuid` or `name`
* `axlGetLine` - required keys: `uuid` or `pattern` or (`pattern`, `routePartitionName`)
* `axlGetLineGroup` -  required keys: `uuid` or `name`
* `axlGetPhone` - required keys: `uuid` or `name`
* `axlGetRemoteDestination` - required keys: `uuid` or `destination`
* `axlGetRemoteDestinationProfile` - required keys: `uuid` or `name`
* `axlGetTranslationPattern` - required keys: `uuid` or `pattern` or (`pattern`, `routePartitionName`)
* `axlGetUser` -  required keys: `uuid` or `userid`

<details>
<summary>Code Example:</summary>

```python
cucm = ...
print("Result:", cucm.axlGetPhone(**{"uuid": "........-....-....-....-............"}))
# Result: {
#     'name': '...',
#     ...,  
#     'lines': {
#         'line': [
#             {
#                 'index': 1,
#                  ...,
#                 'dirn': {
#                     'pattern': '...',
#                     'routePartitionName': {'_value_1': '...', 'uuid': '{........-....-....-....-............}'},
#                     'uuid': '{........-....-....-....-............}'
#                 },
#                 'uuid': '{........-....-....-....-............'
#             }
#         ], 
#         'lineIdentifier': None
#     }, 
#     'uuid': '{........-....-....-....-............}'
# }
```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Remove Methods

* `axlRemoveCallPickupGroup` -  required keys: `uuid` or `name` or `pattern` or (`pattern`, `routePartitionName`)
* `axlRemoveDeviceProfile` -  required keys: `uuid` or `name`
* `axlRemoveLine` - required keys: `uuid` or `pattern` or (`pattern`, `routePartitionName`)
* `axlRemoveLineGroup` -  required keys: `uuid` or `name`
* `axlRemovePhone` - required keys: `uuid` or `name`
* `axlRemoveRemoteDestination` - required keys: `uuid` or `destination`
* `axlRemoveRemoteDestinationProfile` - required keys: `uuid` or `name`
* `axlRemoveTranslationPattern` - required keys: `uuid` or `pattern` or (`pattern`, `routePartitionName`)
* `axlRemoveUser` -  required keys: `uuid` or `userid`

<details>
<summary>Code Example:</summary>

```python
cucm = ...
print("Result:", cucm.axlRemoveLine(**{"uuid": "........-....-....-....-............"}))
# Result: {
#     'return': '{........-....-....-....-............}',
#     'sequence': None
# }
```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Reset Methods

* `axlResetPhone` - required keys: `uuid` or `name`

<details>
<summary>Code Example:</summary>

```python

```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Restart Methods

* `axlRestartPhone` - required keys: `uuid` or `name`

<details>
<summary>Code Example:</summary>

```python

```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Update Methods

* `axlUpdateCallPickupGroup` -  required keys: `uuid` or `name` or `pattern` or (`pattern`, `routePartitionName`)
  <details>
  <summary>expected keys:</summary>
    
  * `newPattern`
  * `description`
  * `newRoutePartitionName`
  * `removeMembers`
  * `addMembers`
  * `members`
  * `pickupNotification`
  * `pickupNotificationTimer`
  * `callInfoForPickupNotification`
  * `newName`
  
  </details>
* `axlUpdateDeviceProfile` -  required keys: `uuid` or `name`
  <details>
  <summary>expected keys:</summary>

  * `newName`
  * `description`
  * `userHoldMohAudioSourceId`
  * `vendorConfig`
  * `mlppDomainId`
  * `mlppIndicationStatus`
  * `preemption`
  * `lines`
  * `phoneTemplateName`
  * `speeddials`
  * `busyLampFields`
  * `blfDirectedCallParks`
  * `addOnModules`
  * `userLocale`
  * `singleButtonBarge`
  * `joinAcrossLines`
  * `loginUserId`
  * `ignorePresentationIndicators`
  * `dndOption`
  * `dndRingSetting`
  * `dndStatus`
  * `emccCallingSearchSpace`
  * `alwaysUsePrimeLine`
  * `alwaysUsePrimeLineForVoiceMessage`
  * `softkeyTemplateName`
  * `callInfoPrivacyStatus`
  * `services`
  * `featureControlPolicy`
  
  </details>
* `axlUpdateLine` -  required keys: `uuid` or `pattern` or (`pattern`, `routePartitionName`)
  <details>
  <summary>expected keys:</summary>

  * `newPattern`
  * `description`
  * `newRoutePartitionName`
  * `aarNeighborhoodName`
  * `aarDestinationMask`
  * `aarKeepCallHistory`
  * `aarVoiceMailEnabled`
  * `callForwardAll`
  * `callForwardBusy`
  * `callForwardBusyInt`
  * `callForwardNoAnswer`
  * `callForwardNoAnswerInt`
  * `callForwardNoCoverage`
  * `callForwardNoCoverageInt`
  * `callForwardOnFailure`
  * `callForwardAlternateParty`
  * `callForwardNotRegistered`
  * `callForwardNotRegisteredInt`
  * `callPickupGroupName`
  * `autoAnswer`
  * `networkHoldMohAudioSourceId`
  * `userHoldMohAudioSourceId`
  * `alertingName`
  * `asciiAlertingName`
  * `presenceGroupName`
  * `shareLineAppearanceCssName`
  * `voiceMailProfileName`
  * `patternPrecedence`
  * `releaseClause`
  * `hrDuration`
  * `hrInterval`
  * `cfaCssPolicy`
  * `defaultActivatedDeviceName`
  * `parkMonForwardNoRetrieveDn`
  * `parkMonForwardNoRetrieveIntDn`
  * `parkMonForwardNoRetrieveVmEnabled`
  * `parkMonForwardNoRetrieveIntVmEnabled`
  * `parkMonForwardNoRetrieveCssName`
  * `parkMonForwardNoRetrieveIntCssName`
  * `parkMonReversionTimer`
  * `partyEntranceTone`
  * `directoryURIs`
  * `allowCtiControlFlag`
  * `rejectAnonymousCall`
  * `patternUrgency`
  * `confidentialAccess`
  * `externalCallControlProfile`
  * `enterpriseAltNum`
  * `e164AltNum`
  * `pstnFailover`
  * `callControlAgentProfile`
  * `useEnterpriseAltNum`
  * `useE164AltNum`
  * `active`

  </details>
* `axlUpdateLineGroup` -  required keys: `uuid` or `name`
  <details>
  <summary>expected keys:</summary>

  * `distributionAlgorithm`
  * `rnaReversionTimeOut`
  * `huntAlgorithmNoAnswer`
  * `huntAlgorithmBusy`
  * `huntAlgorithmNotAvailable`
  * `removeMembers`
  * `addMembers`
  * `members`
  * `newName`
  * `autoLogOffHunt`

  </details>
* `axlUpdatePhone` -  required keys: `uuid` or `name`
  <details>
  <summary>expected keys:</summary>

  * `newName`
  * `description`
  * `callingSearchSpaceName`
  * `devicePoolName`
  * `commonDeviceConfigName`
  * `commonPhoneConfigName`
  * `networkLocation`
  * `locationName`
  * `mediaResourceListName`
  * `networkHoldMohAudioSourceId`
  * `userHoldMohAudioSourceId`
  * `automatedAlternateRoutingCssName`
  * `aarNeighborhoodName`
  * `loadInformation`
  * `vendorConfig`
  * `versionStamp`
  * `traceFlag`
  * `mlppDomainId`
  * `mlppIndicationStatus`
  * `preemption`
  * `useTrustedRelayPoint`
  * `retryVideoCallAsAudio`
  * `securityProfileName`
  * `sipProfileName`
  * `cgpnTransformationCssName`
  * `useDevicePoolCgpnTransformCss`
  * `geoLocationName`
  * `geoLocationFilterName`
  * `sendGeoLocation`
  * `removeLines`
  * `addLines`
  * `lines`
  * `phoneTemplateName`
  * `speeddials`
  * `busyLampFields`
  * `primaryPhoneName`
  * `ringSettingIdleBlfAudibleAlert`
  * `ringSettingBusyBlfAudibleAlert`
  * `blfDirectedCallParks`
  * `addOnModules`
  * `userLocale`
  * `networkLocale`
  * `idleTimeout`
  * `authenticationUrl`
  * `directoryUrl`
  * `idleUrl`
  * `informationUrl`
  * `messagesUrl`
  * `proxyServerUrl`
  * `servicesUrl`
  * `services`
  * `softkeyTemplateName`
  * `defaultProfileName`
  * `enableExtensionMobility`
  * `singleButtonBarge`
  * `joinAcrossLines`
  * `builtInBridgeStatus`
  * `callInfoPrivacyStatus`
  * `hlogStatus`
  * `ownerUserName`
  * `ignorePresentationIndicators`
  * `packetCaptureMode`
  * `packetCaptureDuration`
  * `subscribeCallingSearchSpaceName`
  * `rerouteCallingSearchSpaceName`
  * `allowCtiControlFlag`
  * `presenceGroupName`
  * `unattendedPort`
  * `requireDtmfReception`
  * `rfc2833Disabled`
  * `certificateOperation`
  * `authenticationMode`
  * `keySize`
  * `keyOrder`
  * `ecKeySize`
  * `authenticationString`
  * `upgradeFinishTime`
  * `deviceMobilityMode`
  * `remoteDevice`
  * `dndOption`
  * `dndRingSetting`
  * `dndStatus`
  * `isActive`
  * `mobilityUserIdName`
  * `phoneSuite`
  * `phoneServiceDisplay`
  * `isProtected`
  * `mtpRequired`
  * `mtpPreferedCodec`
  * `dialRulesName`
  * `sshUserId`
  * `sshPwd`
  * `digestUser`
  * `outboundCallRollover`
  * `hotlineDevice`
  * `secureInformationUrl`
  * `secureDirectoryUrl`
  * `secureMessageUrl`
  * `secureServicesUrl`
  * `secureAuthenticationUrl`
  * `secureIdleUrl`
  * `alwaysUsePrimeLine`
  * `alwaysUsePrimeLineForVoiceMessage`
  * `featureControlPolicy`
  * `deviceTrustMode`
  * `earlyOfferSupportForVoiceCall`
  * `requireThirdPartyRegistration`
  * `blockIncomingCallsWhenRoaming`
  * `homeNetworkId`
  * `AllowPresentationSharingUsingBfcp`
  * `confidentialAccess`
  * `requireOffPremiseLocation`
  * `allowiXApplicableMedia`
  * `cgpnIngressDN`
  * `useDevicePoolCgpnIngressDN`
  * `msisdn`
  * `enableCallRoutingToRdWhenNoneIsActive`
  * `wifiHotspotProfile`
  * `wirelessLanProfileGroup`
  * `elinGroup`

  </details>
* `axlUpdateRemoteDestination` -  required keys: `uuid` or `destination`
  <details>
  <summary>expected keys:</summary>

  * `newName`
  * `newDestination`
  * `answerTooSoonTimer`
  * `answerTooLateTimer`
  * `delayBeforeRingingCell`
  * `ownerUserId`
  * `enableUnifiedMobility`
  * `remoteDestinationProfileName`
  * `enableExtendAndConnect`
  * `ctiRemoteDeviceName`
  * `dualModeDeviceName`
  * `isMobilePhone`
  * `enableMobileConnect`
  * `lineAssociations`
  * `timeZone`
  * `todAccessName`
  * `mobileSmartClientName`
  * `mobilityProfileName`
  * `singleNumberReachVoicemail`
  * `dialViaOfficeReverseVoicemail`
  * `removeRingSchedule`
  * `addRingSchedule`
  * `ringSchedule`
  * `accessListName`

  </details>
* `axlUpdateRemoteDestinationProfile` -  required keys: `uuid` or `name`
  <details>
  <summary>expected keys:</summary>

  * `newName`
  * `description`
  * `callingSearchSpaceName`
  * `devicePoolName`
  * `networkHoldMohAudioSourceId`
  * `userHoldMohAudioSourceId`
  * `lines`
  * `callInfoPrivacyStatus`
  * `userId`
  * `ignorePresentationIndicators`
  * `rerouteCallingSearchSpaceName`
  * `cgpnTransformationCssName`
  * `automatedAlternateRoutingCssName`
  * `useDevicePoolCgpnTransformCss`
  * `userLocale`
  * `networkLocale`
  * `primaryPhoneName`
  * `dndOption`
  * `dndStatus`
  * `mobileSmartClientProfileName`

  </details>
* `axlUpdateTranslationPattern` -  required keys: `uuid` or `pattern` or (`pattern`, `routePartitionName`)
  <details>
  <summary>expected keys:</summary>

  * `dialPlanName`
  * `routeFilterName`
  * `newPattern`
  * `description`
  * `newRoutePartitionName`
  * `blockEnable`
  * `calledPartyTransformationMask`
  * `callingPartyTransformationMask`
  * `useCallingPartyPhoneMask`
  * `callingPartyPrefixDigits`
  * `newDialPlanName`
  * `digitDiscardInstructionName`
  * `patternUrgency`
  * `prefixDigitsOut`
  * `newRouteFilterName`
  * `callingLinePresentationBit`
  * `callingNamePresentationBit`
  * `connectedLinePresentationBit`
  * `connectedNamePresentationBit`
  * `patternPrecedence`
  * `provideOutsideDialtone`
  * `callingPartyNumberingPlan`
  * `callingPartyNumberType`
  * `calledPartyNumberingPlan`
  * `calledPartyNumberType`
  * `callingSearchSpaceName`
  * `resourcePriorityNamespaceName`
  * `routeNextHopByCgpn`
  * `routeClass`
  * `callInterceptProfileName`
  * `releaseClause`
  * `useOriginatorCss`
  * `dontWaitForIDTOnSubsequentHops`
  * `isEmergencyServiceNumber`

  </details>
* `axlUpdateUser` -  required keys: `uuid` or `userid`
  <details>
  <summary>expected keys:</summary>

  * `firstName`
  * `displayName`
  * `middleName`
  * `lastName`
  * `newUserid`
  * `password`
  * `pin`
  * `mailid`
  * `department`
  * `manager`
  * `userLocale`
  * `associatedDevices`
  * `primaryExtension`
  * `associatedPc`
  * `associatedGroups`
  * `enableCti`
  * `digestCredentials`
  * `phoneProfiles`
  * `defaultProfile`
  * `presenceGroupName`
  * `subscribeCallingSearchSpaceName`
  * `enableMobility`
  * `enableMobileVoiceAccess`
  * `maxDeskPickupWaitTime`
  * `remoteDestinationLimit`
  * `passwordCredentials`
  * `pinCredentials`
  * `enableEmcc`
  * `ctiControlledDeviceProfiles`
  * `patternPrecedence`
  * `numericUserId`
  * `mlppPassword`
  * `customUserFields`
  * `homeCluster`
  * `imAndPresenceEnable`
  * `serviceProfile`
  * `lineAppearanceAssociationForPresences`
  * `directoryUri`
  * `telephoneNumber`
  * `title`
  * `mobileNumber`
  * `homeNumber`
  * `pagerNumber`
  * `removeExtensionsInfo`
  * `addExtensionsInfo`
  * `extensionsInfo`
  * `selfService`
  * `userProfile`
  * `calendarPresence`
  * `ldapDirectoryName`
  * `userIdentity`
  * `nameDialing`
  * `ipccExtension`
  * `convertUserAccount`
  * `accountType`
  * `authenticationType`
  * `enableUserToHostConferenceNow`
  * `attendeesAccessCode`
  * `zeroHop`

  </details>

<details>
<summary>Code Example:</summary>

```python
cucm = ...
print("Result:", cucm)
# Result: {"uuid": "........-....-....-....-............", ...,} 
```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### SQL Collection


#### Execute Query

<details>
<summary>Code Example:</summary>

```python
cucm = ...
sql_query = """
    SELECT d.pkid, d.name, d.description
    FROM device d
    WHERE d.name LIKE '%your_value%'
"""
print(cucm.sqlExecuteQuery(sql_query=sql_query))
# Result: (
#     {'pkid': '........-....-....-....-............', 'name': 'SEP...', 'description': '...'},
#     {'pkid': '........-....-....-....-............', 'name': 'RDP...', 'description': '...'}, 
#     {'pkid': '........-....-....-....-............', 'name': 'UDP...', 'description': '...'},
#     {'pkid': '........-....-....-....-............', 'name': 'TCT...', 'description': '...'},
#     {'pkid': '........-....-....-....-............', 'name': 'BOT...', 'description': '...'},
#     {'pkid': '........-....-....-....-............', 'name': 'CSF...', 'description': '...'},
#     {'pkid': '........-....-....-....-............', 'name': 'TAB...', 'description': '...'},
#     {'pkid': '........-....-....-....-............', 'name': 'CIPC...', 'description': '...'},
# )
```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Update Query

<details>
<summary>Code Example:</summary>

```python

```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Predefined Queries

<details>

* `List` Methods:
  * `sqlListCallingSearchSpace`
  * `sqlListCredentialPolicy`
  * `sqlListDevicePool`
  * `sqlListDirGroup`
  * `sqlListMediaResourceGroup`
  * `sqlListMediaResourceList`
  * `sqlListPhoneTemplate`
  * `sqlListProcessNode`
  * `sqlListRecordingProfile`
  * `sqlListRegion`
  * `sqlListRoutePartition`
  * `sqlListSoftkeyTemplate`
  * `sqlListTelecasterService`
  * `sqlListTypeClass`
  * `sqlListTypeCountry`
  * `sqlListTypeModel`
  * `sqlListTypeUserLocale`
  * `sqlListUcServiceProfile`
  * `sqlListUcUserProfile`
* `Search` Methods:
  * `sqlSearchCallPickupGroup`
  * `sqlSearchDevice`
  * `sqlSearchEndUser`
  * `sqlSearchLineGroup`
  * `sqlSearchTranspationPattern`

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Create Your Own Methods

<span style="color:#ff0000">**Don't store sensitive information in source code. For example use ".env" file.**</span>

<details>
<summary>Code Example:</summary>

```python
from pathlib import Path
from typing import Union
from tinyCUCM import CucmSettings, cucm_logging


BASE_DIR = Path(__file__).resolve().parent
settings = {
    "pub_fqdn": "cucm.example.com",
    "pub_version": "11.5",
    "user_login": "Your-CUCM-Account",
    "user_password": "You%wILL#&neVeR!gUEss",
    "toolkit_path": BASE_DIR / "axlsqltoolkit",
    "cert_path": BASE_DIR / "cucm.crt",
    "session_verify": False,
    "session_timeout": 15,
}


class CucmAxlCustom(CucmSettings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    @cucm_logging
    def axlYourOwnGetMethod(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Your Own Get Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid"}`
                            or
                            `kwargs = {"name": "name"}`
        :return:
        """

        return self._axl.getCallManager(**kwargs)["return"]

if __name__ == "__main__":
    cucm = CucmAxlCustom(**settings)
    print("Result:", cucm.axlYourOwnGetMethod(**{"uuid": "........-....-....-....-............"}))
    # Result: {
    #     'callManager': {
    #         'name': 'CM_...',
    #         'description': '...',
    #         'autoRegistration': {
    #             'startDn': None,
    #             'endDn': None,
    #             'nextDn': None,
    #             'routePartitionName': {
    #                 '_value_1': None,
    #                 'uuid': None
    #             },
    #             'e164Mask': None,
    #             'autoRegistrationEnabled': None,
    #             'universalDeviceTemplate': {
    #                 '_value_1': None,
    #                 'uuid': None
    #             },
    #             'lineTemplate': {
    #                 '_value_1': None,
    #                 'uuid': None
    #             }
    #         },
    #         'ports': {
    #             'ethernetPhonePort': ...,
    #             'mgcpPorts': {
    #                 'listen': ...,
    #                 'keepAlive': ...
    #             },
    #             'sipPorts': {
    #                 'sipPhonePort': ...,
    #                 'sipPhoneSecurePort': ...
    #             }
    #         },
    #         'processNodeName': {
    #             '_value_1': '...',
    #             'uuid': '{........-....-....-....-............}'
    #         },
    #         'lbmGroup': {
    #             '_value_1': None,
    #             'uuid': None
    #         },
    #         'ctiid': ...,
    #         'uuid': '{........-....-....-....-............}'
    #     }
    # }
```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Luarvick - lu.luarvick@gmail.com

Project Link: [https://github.com/luarvick/tinyCUCM](https://github.com/luarvick/tinyCUCM)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
