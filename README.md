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
          <li><a href="#ris-methods">RIS Methods</a></li>
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

Cisco UCM WSDL Services:

| WSDL File              | Path                                                                               |
|------------------------|------------------------------------------------------------------------------------|
| SOAPMonitorService     | https://x.x.x.x:8443/realtimeservice/services/SOAPMonitorService?wsdl              |
| RisPort                | https://x.x.x.x:8443/realtimeservice/services/RisPort?wsdl                         |
| RisPort70              | https://x.x.x.x:8443/realtimeservice/services/RisPort70?wsdl                       |
| RisService70           | https://x.x.x.x:8443/realtimeservice2/services/RISService70?wsdl                   |
| PerfmonPort            | https://x.x.x.x:8443/perfmonservice/services/PerfmonPort?wsdl                      |
| ControlCenterServices  | https://x.x.x.x:8443/controlcenterservice/services/ControlCenterServicesPort?wsdl  |
| LogCollectionService   | https://x.x.x.x:8443/logcollectionservice/services/LogCollectionPort?wsdl          |
| CDRonDemand            | https://x.x.x.x:8443/CDRonDemandService/services/CDRonDemand?wsdl                  |
| DimeGetFile            | https://x.x.x.x:8443/logcollectionservice/services/DimeGetFileService?wsdl         |

Download `Cisco AXL Toolkit` from the station (`Application` -> `Plugins`) and put it into the folder with your project.\
Copy `RISService70` and create `RISService70.xml` file, put file it into `axlsqltoolkit` folder.\
Create an Cisco UCM application account or local end user with `Standard CCM Super Users` privileges
(Assign access control group to `Your-CUCM-Account`).

### Instance Create

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
    "ris_wsdl_filename": "wsdlRISService70_test.xml", 
}

if __name__ == "__main__":
    cucm = CucmAxlClient(**settings)
    # Get All AXL Method Names
    print("Result:", cucm.axlAllMethods())
    # Result: (
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

* `axlDoAuthenticateUser` - required keywords args: (`userid`, `password`) or (`userid`, `pin`)
* `axlDoDeviceLogin` - required keywords args: (`deviceName`, `loginDuration`, `profileName`, `userId`)
  * Arg `loginDuration: str` values:
    * `"0"` - Logout disabled
    * `"36000"` - Logout after 10h
* `axlDoDeviceLogout` - required keywords args: `deviceName`
* `axlDoLdapSync` - required keywords args: (`uuid`, `sync`) or (`name`, `sync`)
  * Arg `sync: bool` values:
    * `True` - Start Synchronization
    * `False` - Cancel the Synchronization which is currently under process

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

* `axlGetCallPickupGroup` - required keywords args: `uuid` or `name` or `pattern` or (`pattern`, `routePartitionName`)
* `axlGetDeviceProfile` - required keywords args: `uuid` or `name`
* `axlGetLine` - required keywords args: `uuid` or `pattern` or (`pattern`, `routePartitionName`)
* `axlGetLineGroup` - required keywords args: `uuid` or `name`
* `axlGetPhone` - required keywords args: `uuid` or `name`
* `axlGetRemoteDestination` - required keywords args: `uuid` or `destination`
* `axlGetRemoteDestinationProfile` - required keywords args: `uuid` or `name`
* `axlGetTranslationPattern` - required keywords args: `uuid` or `pattern` or (`pattern`, `routePartitionName`)
* `axlGetUser` - required keywords args: `uuid` or `userid`

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

* `axlRemoveCallPickupGroup` - required keywords args: `uuid` or `name` or `pattern` or (`pattern`, `routePartitionName`)
* `axlRemoveDeviceProfile` - required keywords args: `uuid` or `name`
* `axlRemoveLine` - required keywords args: `uuid` or `pattern` or (`pattern`, `routePartitionName`)
* `axlRemoveLineGroup` - required keywords args: `uuid` or `name`
* `axlRemovePhone` - required keywords args: `uuid` or `name`
* `axlRemoveRemoteDestination` - required keywords args: `uuid` or `destination`
* `axlRemoveRemoteDestinationProfile` - required keywords args: `uuid` or `name`
* `axlRemoveTranslationPattern` - required keywords args: `uuid` or `pattern` or (`pattern`, `routePartitionName`)
* `axlRemoveUser` - required keywords args: `uuid` or `userid`

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

* `axlResetPhone` - required keywords args: `uuid` or `name`

<details>
<summary>Code Example:</summary>

```python

```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Restart Methods

* `axlRestartPhone` - required keywords args: `uuid` or `name`

<details>
<summary>Code Example:</summary>

```python

```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### RIS Methods

RIS - Real-time Information Server retrieve information stored in all RIS nodes in the cluster.
https://developer.cisco.com/docs/sxml/#!risport70-api

* `risGetCti` - required keywords args: `collection_name`, `items_collection`, `cti_mgr_class`
  * Arg `collection_name` values: `DevNames` or `DirNumbers`
  * Arg `items_collection`: Collection of Dictionaries. Depending on the type of collection, dictionaries should
    contain the key `name` for `DevNames` or the key `pattern` for `DirNumbers`
  * Arg `cti_mgr_class` values: `Provider` or `Device` or `Line`
* `risGetPhone` - required keywords args: `phone_name`
* `risGetPhones` - required keywords args: `devices_collection`
  * Arg `devices_collection` - Collection of Dictionaries. Dictionaries should contain the key `name`

<details>
<summary>Code Example:</summary>

```python
cucm = ...
print("Result:", cucm.risGetCti(
    collection_name="DirNumbers",
    items_collection=({"pattern": "..."}, {"pattern": "..."}, ...),
    cti_mgr_class="Line"
))
# Result: {
#     'SelectCtiItemResult': {
#         'TotalItemsFound': 6,
#         'CtiNodes': {...}
#     },
#     'StateInfo': '<StateInfo><Node Name="cucm.example.com" ...'
# } 

print("Result:", cucm.risGetPhone(phone_name="CSF...", is_raw_resp=False))
# Result: {
#     'DeviceName': 'CSF...',
#     'Status': 'Registered',
#     'Model': 503,
#     'Product': 390,
#     'IP': 'xxx.xxx.xxx.xxx',
#     'NodeName': 'cucm.example.com',
#     'ActiveLoadID': '...',
#     'InactiveLoadID': '...'
# }

print("Result:", cucm.risGetPhones(devices_collection=({"name": "TCT..."}, {"name": "CSF..."}, ...), is_raw_resp=False))
# Result = (
#     {
#         'name': 'TCT...',
#         'ris': {
#             'DeviceName': 'TCT...',
#             'Status': 'UnRegistered',
#             'Model': 562,
#             'Product': 449,
#             'IP': 'xxx.xxx.xxx.xxx',
#             'NodeName': 'cucm.example.com',
#             'ActiveLoadID': '...',
#             'InactiveLoadID': '...'
#         }
#     },
#     {
#         'name': 'CSF...',
#         'ris': {
#             'DeviceName': 'CSF...',
#             'Status': 'Registered',
#             'Model': 503,
#             'Product': 390,
#             'IP': 'xxx.xxx.xxx.xxx',
#             'NodeName': 'cucm.example.com',
#             'ActiveLoadID': '...',
#             'InactiveLoadID': '...'
#         }
#     },
#     {
#         'name': 'SEP...',
#         'ris': {'DeviceName': None, 'Status': None, ...}
#     },
#     {
#         'name': 'RDP...',
#         'ris': {'DeviceName': None, 'Status': None, ...}
#     },
#     {
#         'name': 'UDP...',
#         'ris': {'DeviceName': None, 'Status': None, ...}
#     }
# )
```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Update Methods

* `axlUpdateCallPickupGroup` - required keywords args: `uuid` or `name` or `pattern` or (`pattern`, `routePartitionName`)
  <details>
  <summary>expected keywords args:</summary>
    
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
* `axlUpdateDeviceProfile` - required keywords args: `uuid` or `name`
  <details>
  <summary>expected keywords args:</summary>

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
* `axlUpdateLine` - required keywords args: `uuid` or `pattern` or (`pattern`, `routePartitionName`)
  <details>
  <summary>expected keywords args:</summary>

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
* `axlUpdateLineGroup` - required keywords args: `uuid` or `name`
  <details>
  <summary>expected keywords args:</summary>

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
* `axlUpdatePhone` - required keywords args: `uuid` or `name`
  <details>
  <summary>expected keywords args:</summary>

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
* `axlUpdateRemoteDestination` - required keywords args: `uuid` or `destination`
  <details>
  <summary>expected keywords args:</summary>

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
* `axlUpdateRemoteDestinationProfile` - required keywords args: `uuid` or `name`
  <details>
  <summary>expected keywords args:</summary>

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
* `axlUpdateTranslationPattern` - required keywords args: `uuid` or `pattern` or (`pattern`, `routePartitionName`)
  <details>
  <summary>expected keywords args:</summary>

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
* `axlUpdateUser` - required keywords args: `uuid` or `userid`
  <details>
  <summary>expected keywords args:</summary>

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
print("Result:", cucm.axlUpdatePhone(**{"uuid": "........-....-....-....-............", "description": "New Description"}))
# Result: {
#     'return': '{........-....-....-....-............}',
#     'sequence': None
# }
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
    WHERE d.name LIKE '%value%'
"""
print("Result:", cucm.sqlExecuteQuery(sql_query=sql_query))
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
cucm = ...
sql_query = """
    UPDATE device d 
    SET d.description = 'New Description via SQL' 
    WHERE d.name LIKE '%value%'
"""
print("Result:", cucm.sqlUpdateQuery(sql_query=sql_query))
# Result: {
#     'return': {
#         'rowsUpdated': 1
#     },
#     'sequence': None
# }
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
  * `sqlSearchCallPickupGroup` - required keywords args: `criterion`, `value`
    * Arg `criterion`: `Name`, `Description`, `Pattern`, `Member Line Number`, `Member Line Description`
  * `sqlSearchDevice` - required keywords args: `criterion`, `value`
    * Arg `criterion`: `Name`, `Description`, `Line Number`, `Line Description`, `Userid`, `Device Pool`,
      `Device Type`
  * `sqlSearchEndUser` - required keywords args: `criterion`, `value`
    * Arg `criterion`: `Userid`, `Display Name`, `Last Name`, `First Name`, `Phone Number`, `Mobile Number`,
      `Email`, `Directory URI`
  * `sqlSearchLineGroup` - required keywords args: `criterion`, `value`
    * Arg `criterion`: `Name`, `Member Line Number`, `Member Line Description`
  * `sqlSearchTranslationPattern` - required keywords args: `criterion`, `value`
    * Arg `criterion`: `Pattern`, `Description`, `Partition`, `Calling Search Space`, `Called Party Transform Mask`,
      `Prefix Digits Out` 
* `Validate` Methods:
  * `sqlValidateDeviceEndUserDesignation` - required keywords args: `device` (Type Class: Any)
  * `sqlValidateLine` - required keywords args: `pattern` (Type Pattern Usage: Device Only)
  * `sqlValidatePattern` - required keywords args: `pattern` (Type Pattern Usage: Any)

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
    "ris_wsdl_filename": "wsdlRISService70_test.xml", 
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
    #         'autoRegistration': {...},
    #         'ports': {...},
    #         'processNodeName': {...},
    #         'lbmGroup': {...},
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
