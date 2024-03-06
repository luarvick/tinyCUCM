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
        <li><a href="#ccs-methods">CCS Methods</a></li>
        <li><a href="#ris-methods">RIS Methods</a></li>
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


## About The Project

This project is for informational purposes only and is intended to study the capabilities of the Cisco Unified Call Manager's API. 
Methods have been tested on CUCM ver. 11.5.\
[Cisco UCM AXL Schemas & SQL Data Dictionaries Documentation](https://developer.cisco.com/docs/axl/#!archived-references)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Installation

Installation is as simple as:

   ```sh
   pip install tinyCUCM
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


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
from tinyCUCM import CucmClient


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
    cucm = CucmClient(**settings)
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

* `axlAddCallPickupGroup`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `callPickupGroup`
    * `name`
    * `pattern`
  * expected:
    * `description`
    * `routePartitionName`
    * `members`
    * `pickupNotification`
    * `pickupNotificationTimer`
    * `callInfoForPickupNotification`
  </details>
* `axlAddDeviceProfile`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `deviceProfile`
    * `name`
    * `product`
    * `class`
    * `protocol`
    * `protocolSide`
    * `phoneTemplateName`
  * expected:
    * `name`
    * `description`
    * `userHoldMohAudioSourceId`
    * `vendorConfig`
    * `traceFlag`
    * `mlppDomainId`
    * `mlppIndicationStatus`
    * `preemption`
    * `lines`
      * `line` - collection of:
        * required:
          * `index`
          * `dirn`
            * `pattern`
            * `routePartitionName`
        * expected:
          * `label`
          * `display`
          * `ringSetting`
          * `consecutiveRingSetting`
          * `ringSettingIdlePickupAlert`
          * `ringSettingActivePickupAlert`
          * `displayAscii`
          * `e164Mask`
          * `mwlPolicy`
          * `maxNumCalls`
          * `busyTrigger`
          * `callInfoDisplay`
          * `recordingProfileName`
          * `monitoringCssName`
          * `recordingFlag`
          * `audibleMwi`
          * `speedDial`
          * `partitionUsage`
          * `associatedEndusers`
          * `missedCallLogging`
          * `recordingMediaSource`
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
* `axlAddLine`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `line`
    * `pattern`
    * `usage`
  * expected:
    * `description`
    * `routePartitionName`
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
* `axlAddLineGroup`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `lineGroup`
    * `name`
    * `distributionAlgorithm`
    * `rnaReversionTimeOut`
    * `huntAlgorithmNoAnswer`
    * `huntAlgorithmBusy`
    * `huntAlgorithmNotAvailable`
  * expected:
    * `members`
    * `autoLogOffHunt`
  </details>
* `axlAddPhone`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `phone`
    * `name`
    * `product`
    * `class`
    * `protocol`
    * `protocolSide`
    * `devicePoolName`
    * `commonPhoneConfigName`
    * `locationName`
    * `useTrustedRelayPoint`
    * `phoneTemplateName`
    * `primaryPhoneName`
    * `builtInBridgeStatus`
    * `packetCaptureMode`
    * `certificateOperation`
    * `deviceMobilityMode`
  * expected:
    * `description`
    * `callingSearchSpaceName`
    * `commonDeviceConfigName`
    * `networkLocation`
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
    * `retryVideoCallAsAudio`
    * `securityProfileName`
    * `sipProfileName`
    * `cgpnTransformationCssName`
    * `useDevicePoolCgpnTransformCss`
    * `geoLocationName`
    * `geoLocationFilterName`
    * `sendGeoLocation`
    * `lines`
      * `line` - collection of:
        * required:
          * `index`
          * `dirn`
            * `pattern`
            * `routePartitionName`
        * expected:
          * `label`
          * `display`
          * `ringSetting`
          * `consecutiveRingSetting`
          * `ringSettingIdlePickupAlert`
          * `ringSettingActivePickupAlert`
          * `displayAscii`
          * `e164Mask`
          * `mwlPolicy`
          * `maxNumCalls`
          * `busyTrigger`
          * `callInfoDisplay`
          * `recordingProfileName`
          * `monitoringCssName`
          * `recordingFlag`
          * `audibleMwi`
          * `speedDial`
          * `partitionUsage`
          * `associatedEndusers`
          * `missedCallLogging`
          * `recordingMediaSource`
    * `speeddials`
    * `busyLampFields`
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
    * `callInfoPrivacyStatus`
    * `hlogStatus`
    * `ownerUserName`
    * `ignorePresentationIndicators`
    * `packetCaptureDuration`
    * `subscribeCallingSearchSpaceName`
    * `rerouteCallingSearchSpaceName`
    * `allowCtiControlFlag`
    * `presenceGroupName`
    * `unattendedPort`
    * `requireDtmfReception`
    * `rfc2833Disabled`
    * `authenticationMode`
    * `keySize`
    * `keyOrder`
    * `ecKeySize`
    * `authenticationString`
    * `upgradeFinishTime`
    * `remoteDevice`
    * `dndOption`
    * `dndRingSetting`
    * `dndStatus`
    * `isActive`
    * `isDualMode`
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
* `axlAddeRemoteDestination`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `remoteDestination`
    * `destination`
    * `answerTooSoonTimer`
    * `answerTooLateTimer`
    * `delayBeforeRingingCell`
    * `ownerUserId`
    * `remoteDestinationProfileName`
  * expected:
    * `name`
    * `enableUnifiedMobility`
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
    * `ringSchedule`
    * `accessListName`
  </details>
* `axlAddRemoteDestinationProfile`
  <details>
  <summary>keywords args</summary>

  * required:
    * `remoteDestinationProfile`
    * `name`
    * `product`
    * `class`
    * `protocol`
    * `protocolSide`
    * `devicePoolName`
    * `callInfoPrivacyStatus`
    * `userId`
  * expected:
    * `description`
    * `callingSearchSpaceName`
    * `networkHoldMohAudioSourceId`
    * `userHoldMohAudioSourceId`
    * `lines`
      * `line` - collection of:
        * required:
          * `index`
          * `dirn`
            * `pattern`
            * `routePartitionName`
        * expected:
          * `label`
          * `display`
          * `ringSetting`
          * `consecutiveRingSetting`
          * `ringSettingIdlePickupAlert`
          * `ringSettingActivePickupAlert`
          * `displayAscii`
          * `e164Mask`
          * `mwlPolicy`
          * `maxNumCalls`
          * `busyTrigger`
          * `callInfoDisplay`
          * `recordingProfileName`
          * `monitoringCssName`
          * `recordingFlag`
          * `audibleMwi`
          * `speedDial`
          * `partitionUsage`
          * `associatedEndusers`
          * `missedCallLogging`
          * `recordingMediaSource`
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
* `axlAddTranslationPattern`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `transPattern`
    * `pattern`
    * `routePartitionName`
    * `usage`
  * expected:
    * `description`
    * `blockEnable`
    * `calledPartyTransformationMask`
    * `callingPartyTransformationMask`
    * `useCallingPartyPhoneMask`
    * `callingPartyPrefixDigits`
    * `dialPlanName`
    * `digitDiscardInstructionName`
    * `patternUrgency`
    * `prefixDigitsOut`
    * `routeFilterName`
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
* `axlAddUser`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `user`
    * `userid`
    * `lastName`
    * `presenceGroupName`
  * expected:
    * `firstName`
    * `displayName`
    * `middleName`
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
print("Result:", cucm.axlAddCallPickupGroup(**{"callPickupGroup": {"name": "...", "pattern": "..."}}))
# Result: {'return': '{........-....-....-....-............}', 'sequence': None}

print("Result:", cucm.axlAddLine(**{"line": {"pattern": "...", "usage": "Device"}}))
# Result: {'return': '{........-....-....-....-............}', 'sequence': None}

print("Result:", cucm.axlAddLineGroup(**{
    "lineGroup": {
        "name": "...",
        "distributionAlgorithm": "Broadcast",
        "rnaReversionTimeOut": 10,
        "huntAlgorithmNoAnswer": "Try next member; then, try next group in Hunt List",
        "huntAlgorithmBusy": "Try next member; then, try next group in Hunt List",
        "huntAlgorithmNotAvailable": "Try next member; then, try next group in Hunt List",
    }
}))
# Result: {'return': '{........-....-....-....-............}', 'sequence': None}

print("Result:", cucm.axlAddPhone(**{
    "phone": {
        "name": "...",
        "product": "Cisco 7821",
        "class": "Phone",
        "protocol": "SIP",
        "protocolSide": "User",
        "devicePoolName": "Default",
        "commonPhoneConfigName": "Standard Common Phone Profile",
        "locationName": "Hub_None",
        "useTrustedRelayPoint": "Default",
        "phoneTemplateName": "Standard 7821 SIP",
        "primaryPhoneName": None,
        "builtInBridgeStatus": "Default",
        "packetCaptureMode": "None",
        "certificateOperation": "No Pending Operation",
        "deviceMobilityMode": "Default"
    }
}))
# Result: {'return': '{........-....-....-....-............}', 'sequence': None}

print("Result:", cucm.axlAddRemoteDestination(**{
    "remoteDestination": {
        "destination": "...",
        "answerTooSoonTimer": 1500,
        "answerTooLateTimer": 19000,
        "delayBeforeRingingCell": 4000,
        "ownerUserId": "...",
        "remoteDestinationProfileName": "..."
    }
}))
# Result: <Response [200]>

print("Result:", cucm.axlAddRemoteDestinationProfile(**{
    "remoteDestinationProfile": {
        "name": "...",
        "product": "Remote Destination Profile",
        "class": "Remote Destination Profile",
        "protocol": "Remote Destination",
        "protocolSide": "User",
        "devicePoolName": "...",
        "callInfoPrivacyStatus": "Default",
        "userId": "..."
    }
}))
# Result: {'return': '{........-....-....-....-............}', 'sequence': None}

# Pattern without `routePartitionName`
print("Result:", cucm.axlAddTranslationPattern(**{
        "transPattern": {"pattern": "...", "routePartitionName": "", "usage": "Translation"}
}))
# Result: {'return': '{........-....-....-....-............}', 'sequence': None}

print("Result:", cucm.axlAddUser(**{
  "user": {"userid": "...", "lastName": "...", "presenceGroupName": "Standard Presence group"}
}))
# Result: {'return': '{........-....-....-....-............}', 'sequence': None}
```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Do Methods

* `axlDoAuthenticateUser`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `userid`
    * `password` or `pin`
  </details>
* `axlDoDeviceLogin`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `deviceName`
    * `loginDuration`
      * `"0"` - Logout disabled
      * `"36000"` - Logout after 10h (or any other positive value in milliseconds)
    * `profileName`
    * `userId`
  </details>
* `axlDoDeviceLogout`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `deviceName`
  </details>
* `axlDoLdapSync`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `name`
    * `sync`
      * `True` - Start Synchronization
      * `False` - Cancel the Synchronization which is currently under process
  </details>

<details>
<summary>Code Example:</summary>

```python
cucm = ...
print("Result:", cucm.axlDoAuthenticateUser(userid="...", pin= "..."))
print("Result:", cucm.axlDoAuthenticateUser(**{"userid": "...", "password": "..."}))
# Result: {'return': {'userAuthenticated': 'true', 'code': 0, 'daysToExpiry': 0, 'isWarningNeeded': 'false'}, 'sequence': None}
# Result: {'return': {'userAuthenticated': 'false', 'code': 1, 'daysToExpiry': 0, 'isWarningNeeded': 'false'}, 'sequence': None}

print("Result:", cucm.axlDoDeviceLogin(**{"deviceName": "SEP...", "loginDuration": "...", "profileName":"...", "userid": "..."}))
# Result: {'return': '{........-....-....-....-............}', 'sequence': None}

print("Result:", cucm.axlDoDeviceLogout(**{"deviceName": "SEP..."}))
# Result: {'return': '{........-....-....-....-............}', 'sequence': None}

print("Result:", cucm.axlDoLdapSync(**{"uuid": "........-....-....-....-............", "sync": True}))
# Result: {'return': 'Sync initiated successfully', 'sequence': None}
```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Get Methods

* `axlGetCallPickupGroup`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `name` or `pattern` or (`pattern`, `routePartitionName`)
  </details>
* `axlGetDeviceProfile`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `name`
  </details>
* `axlGetLine`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `pattern` or (`pattern`, `routePartitionName`)
  </details>
* `axlGetLineGroup`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `name`
  </details>
* `axlGetPhone`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `name`
  </details>
* `axlGetRemoteDestination`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `destination`
  </details>
* `axlGetRemoteDestinationProfile`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `name`
  </details>
* `axlGetTranslationPattern`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `pattern` or (`pattern`, `routePartitionName`)
  </details>
* `axlGetUser`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `userid`
  </details>

<details>
<summary>Code Example:</summary>

```python
cucm = ...
print("Result:", cucm.axlGetPhone(name="SEP..."))
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

* `axlRemoveCallPickupGroup`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `name` or `pattern` or (`pattern`, `routePartitionName`)
  </details>
* `axlRemoveDeviceProfile`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `name`
  </details>
* `axlRemoveLine`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `pattern` or (`pattern`, `routePartitionName`)
  </details>
* `axlRemoveLineGroup`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `name`
  </details>
* `axlRemovePhone`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `name`
  </details>
* `axlRemoveRemoteDestination`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `destination`
  </details>
* `axlRemoveRemoteDestinationProfile`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `name`
  </details>
* `axlRemoveTranslationPattern`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `pattern` or (`pattern`, `routePartitionName`)
  </details>
* `axlRemoveUser`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `userid`
  </details>

<details>
<summary>Code Example:</summary>

```python
cucm = ...
print("Result:", cucm.axlRemovePhone(name= "SEP..."))
print("Result:", cucm.axlRemovePhone(**{"uuid": "........-....-....-....-............"}))
# Result: {'return': '{........-....-....-....-............}', 'sequence': None}
```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Reset Methods

* `axlResetPhone`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `name`
  </details>

<details>
<summary>Code Example:</summary>

```python
cucm = ...
print("Result:", cucm.axlResetPhone(name="SEP..."))
print("Result:", cucm.axlResetPhone(**{"uuid": "........-....-....-....-............"}))
# Result: {'return': '{........-....-....-....-............}', 'sequence': None}
```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Restart Methods

* `axlRestartPhone`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `name`
  </details>

<details>
<summary>Code Example:</summary>

```python
cucm = ...
print("Result:", cucm.axlRestartPhone(name="SEP..."))
print("Result:", cucm.axlRestartPhone(**{"uuid": "........-....-....-....-............"}))
# Result: {'return': '{........-....-....-....-............}', 'sequence': None}
```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


#### Update Methods

* `axlUpdateCallPickupGroup`
  <details>
    <summary>keywords args</summary>
  
  * required:
    * `uuid` or `name` or `pattern` or (`pattern`, `routePartitionName`)
  * expected:
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
* `axlUpdateDeviceProfile`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `name`
  * expected:
    * `newName`
    * `description`
    * `userHoldMohAudioSourceId`
    * `vendorConfig`
    * `mlppDomainId`
    * `mlppIndicationStatus`
    * `preemption`
    * `lines`
      * `line` - collection of:
        * required:
          * `index`
          * `dirn`
            * `pattern`
            * `routePartitionName`
        * expected:
          * `label`
          * `display`
          * `ringSetting`
          * `consecutiveRingSetting`
          * `ringSettingIdlePickupAlert`
          * `ringSettingActivePickupAlert`
          * `displayAscii`
          * `e164Mask`
          * `mwlPolicy`
          * `maxNumCalls`
          * `busyTrigger`
          * `callInfoDisplay`
          * `recordingProfileName`
          * `monitoringCssName`
          * `recordingFlag`
          * `audibleMwi`
          * `speedDial`
          * `partitionUsage`
          * `associatedEndusers`
          * `missedCallLogging`
          * `recordingMediaSource`
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
* `axlUpdateLine
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `pattern` or (`pattern`, `routePartitionName`)
  * expected:
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
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `name`
  * expected:
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
* `axlUpdatePhone`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `name`
  * expected:
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
      * `line` - collection of:
        * required:
          * `index`
          * `dirn`
            * `pattern`
            * `routePartitionName`
        * expected:
          * `label`
          * `display`
          * `ringSetting`
          * `consecutiveRingSetting`
          * `ringSettingIdlePickupAlert`
          * `ringSettingActivePickupAlert`
          * `displayAscii`
          * `e164Mask`
          * `mwlPolicy`
          * `maxNumCalls`
          * `busyTrigger`
          * `callInfoDisplay`
          * `recordingProfileName`
          * `monitoringCssName`
          * `recordingFlag`
          * `audibleMwi`
          * `speedDial`
          * `partitionUsage`
          * `associatedEndusers`
          * `missedCallLogging`
          * `recordingMediaSource`
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
* `axlUpdateRemoteDestination`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `destination`
  * expected:
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
* `axlUpdateRemoteDestinationProfile`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `name`
  * expected:
    * `newName`
    * `description`
    * `callingSearchSpaceName`
    * `devicePoolName`
    * `networkHoldMohAudioSourceId`
    * `userHoldMohAudioSourceId`
    * `lines`
      * `line` - collection of:
        * required:
          * `index`
          * `dirn`
            * `pattern`
            * `routePartitionName`
        * expected:
          * `label`
          * `display`
          * `ringSetting`
          * `consecutiveRingSetting`
          * `ringSettingIdlePickupAlert`
          * `ringSettingActivePickupAlert`
          * `displayAscii`
          * `e164Mask`
          * `mwlPolicy`
          * `maxNumCalls`
          * `busyTrigger`
          * `callInfoDisplay`
          * `recordingProfileName`
          * `monitoringCssName`
          * `recordingFlag`
          * `audibleMwi`
          * `speedDial`
          * `partitionUsage`
          * `associatedEndusers`
          * `missedCallLogging`
          * `recordingMediaSource`
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
* `axlUpdateTranslationPattern`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `pattern` or (`pattern`, `routePartitionName`)
  * expected:
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
* `axlUpdateUser`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `uuid` or `userid`
  * expected:
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
print("Result:", cucm.axlUpdatePhone(name="SEP", description="New Description"))
print("Result:", cucm.axlUpdatePhone(**{"uuid": "........-....-....-....-............", "description": "New Description"}))
# Result: {'return': '{........-....-....-....-............}', 'sequence': None}
```

</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### CCS Methods

CCS - Control Center Services provides an API Methods used to view status, to restart, to start and stop Cisco CallManager services for a particular server.

* `ccsDoControlServices`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `control_command` - Control Command: `Restart`, `Start` or `Stop`
    * `service_names` - Service Names Collection
  * optional
    * `node_fqdn` - Specify a node other than the publisher
  </details>
* `ccsDoServiceDeployment`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `deploy_command` - Deploy Command: `Deploy` or `UnDeploy`
    * `service_names` - Service Names Collection
  * optional
    * `node_fqdn` - Specify a node other than the publisher
  </details>
* `ccsGetProductInfoList`
  <details>
  <summary>keywords args</summary>
  
  * optional
    * `node_fqdn` - Specify a node other than the publisher
  </details>
* `ccsGetServiceStatus`
  <details>
  <summary>keywords args</summary>
  
  * optional
    * `service_name` - Specify a specific service name
    * `node_fqdn` - Specify a node other than the publisher
  </details>
* `ccsGetStaticServiceList`
  <details>
  <summary>keywords args</summary>
  
  * optional
    * `node_fqdn` - Specify a node other than the publisher
  </details>

```python
cucm = ...
print("Result:", cucm.ccsDoControlServices(control_command="Restart", service_names=["Cisco License Manager", "Cisco Tftp"]))
# Result: (
#   {'ServiceName': 'Cisco License Manager', 'ServiceStatus': 'Starting', 'ReasonCode': -1, 'ReasonCodeString': ' ', 'StartTime': None, 'UpTime': -1}, 
#   {'ServiceName': 'Cisco Tftp', 'ServiceStatus': 'Started', 'ReasonCode': -1, 'ReasonCodeString': ' ', 'StartTime': 'Tue Mar  5 15:53:19 2024', 'UpTime': 4}
# )

print("Result:", cucm.ccsDoServiceDeployment(deploy_command="Deploy", service_names=["Cisco Tftp"]))
# Result: (
#   {'ServiceName': 'Cisco Tftp', 'ServiceStatus': 'Started', 'ReasonCode': -1, 'ReasonCodeString': ' ', 'StartTime': 'Wed Mar  6 13:37:59 2024', 'UpTime': 17},
# )

print("Result:", cucm.ccsGetServiceStatus())
# Result: (
#   {'ServiceName': 'A Cisco DB', 'ServiceStatus': 'Started', 'ReasonCode': -1, 'ReasonCodeString': ' ', 'StartTime': 'Tue Mar  5 13:01:39 2024', 'UpTime': 10012}, 
#   ...,
#   {'ServiceName': 'Cisco Wireless Controller Synchronization Service', 'ServiceStatus': 'Stopped', 'ReasonCode': -1068, 'ReasonCodeString': 'Service Not Activated ', 'StartTime': None, 'UpTime': -1}
# )


```


### RIS Methods

RIS - Real-time Information Server retrieve information stored in all RIS nodes in the cluster.
https://developer.cisco.com/docs/sxml/#!risport70-api

* `risGetCti`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `collection_name` - values: `DevNames` or `DirNumbers`
    * `items_collection` - Collection of Dictionaries. Depending on the type of collection, dictionaries should
       contain the key `name` for `DevNames` or the key `pattern` for `DirNumbers`
    * `cti_mgr_class` - values: `Provider` or `Device` or `Line`
  </details>
* `risGetPhone`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `phone_name`
  </details>
* `risGetPhones`
  <details>
  <summary>keywords args</summary>
  
  * required:
    * `devices_collection` - Collection of Dictionaries. Dictionaries should contain the key `name`
  </details>

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
    def axlYourOwnGetMethod(self, **kwargs: Union[dict, ...]) -> dict:

        """
        AXL Your Own `Get` or Any Other Method.
        :param kwargs:      Required Fields:
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


## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Contact

Luarvick - lu.luarvick@gmail.com

Project Link: [https://github.com/luarvick/tinyCUCM](https://github.com/luarvick/tinyCUCM)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
