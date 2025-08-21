from collections.abc import Iterable
from datetime import datetime
from random import choice
from typing import Any, Dict, Optional, Tuple, Union
from typing_extensions import Unpack
from uuid import UUID
from zeep.helpers import serialize_object

from .ccs_models import CucmCcsDoControlModel, CucmCcsDoDeploymentModel
from .decorators import cucm_logging
from .settings import CucmSettings
from .ris_models import CucmRisGetCtiModel
from .sql_models import (
    CucmSqlSearchCallPickupGroupModel,
    CucmSqlSearchDeviceModel,
    CucmSqlSearchDirectoryNumberModel,
    CucmSqlSearchEndUserModel,
    CucmSqlSearchLineGroupModel,
    CucmSqlSearchRemoteDestinationModel,
    CucmSqlSearchTranslationPatternModel,
)


""" ######################################################### """
""" ******************** TINY CUCM CLIENT ******************* """
""" ######################################################### """


class CucmClient(CucmSettings):

    """
        tinyCUCM Client. Cisco Unified Call Manager API Methods Collection.
        """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def __cucm_element_list_to_tuple_of_dicts(elements: Iterable) -> tuple[dict, ...]:

        """
        Normalizing `lxml.etree` items.
        :param elements:    Collection of `lxml.etree` Items
        :return:
        """

        return tuple([{item.tag: item.text for item in row} for row in elements])

    @staticmethod
    def __cucm_ris_phone_resp_normalizing(resp_raw: dict) -> tuple[dict, ...]:

        """
        Normalizing RIS (Real-time Information Server) Phone(s) Response Dictionary.
        :param resp_raw:    RIS Raw Response Dictionary
        :return:
        """

        resp_result = []
        if resp_raw["SelectCmDeviceResult"]["TotalDevicesFound"] > 0:
            # Devices can be Registered, UnRegistered, Rejected, PartiallyRegistered, Unknown
            for item in resp_raw["SelectCmDeviceResult"]["CmNodes"]["item"]:
                if item["ReturnCode"] == "Ok":
                    for device in item["CmDevices"]["item"]:
                        # CTI Remote Device (Type Model d.tkmodel = "635") no IPAddress
                        resp_result.append(
                            {
                                "DeviceName": device["Name"],
                                "Status": device["Status"],
                                "Model": device["Model"],
                                "Product": device["Product"],
                                "IP": device["IPAddress"]["item"][0]["IP"] if device["IPAddress"] else None,
                                "NodeName": item["Name"],
                                "ActiveLoadID": device["ActiveLoadID"],
                                "InactiveLoadID": device["InactiveLoadID"]
                            }
                        )
        else:
            # For 'risGetPhone' - Device not found (Not exist, Off-line, Unsupported Class or Type (RDP, UDP and ect.))
            resp_result.append(
                {
                    "DeviceName": None,
                    "Status": None,
                    "Model": None,
                    "Product": None,
                    "IP": None,
                    "NodeName": None,
                    "ActiveLoadID": None,
                    "InactiveLoadID": None
                })
        return tuple(resp_result)

    def __cucm_sql_serialize_to_tuple(self, resp_raw) -> Union[tuple[dict, ...], None]:

        """
        Serialize collection of `lxml.etree` items from the SQL Response to the tuple of dictionaries.
        :param resp_raw:    SQL Query Response (class `zeep.objects.ExecuteSQLQueryRes`)
        :return:
        """

        try:
            resp_result = self.__cucm_element_list_to_tuple_of_dicts(serialize_object(resp_raw["return"]["rows"]))
        except KeyError:
            # Single Tuple Response
            resp_result = self.__cucm_element_list_to_tuple_of_dicts(serialize_object(resp_raw["return"]["row"]))
        except TypeError:
            # No SQL Tuples: {'return': None, 'sequence': None} -> None
            resp_result = serialize_object(resp_raw["return"])
        return resp_result

    @cucm_logging
    def __cucm_sql_execute(self, sql_query: str) -> Union[tuple[dict, ...], None]:

        """
        Base AXL SQL Execute method for request to the Cisco UCM DB Informix.
        :param sql_query:   SQL Query Expression
        :return:
        """

        return self.__cucm_sql_serialize_to_tuple(self._axl.executeSQLQuery(sql=sql_query))

    @cucm_logging
    def axlAllMethods(self) -> tuple[str, ...]:

        """
        AXL All Methods Collection.
        :return:
        """

        return tuple(sorted([str(method[0]) for method in self._axl]))

    @cucm_logging
    def ccsAllMethods(self) -> tuple[str, ...]:

        """
        CCS All Methods Collection.
        :return:
        """

        return tuple(sorted([str(method[0]) for method in self._ccs]))

    @cucm_logging
    def risAllMethods(self) -> tuple[str, ...]:

        """
        RIS (Real-time Information Server) All Methods Collection.
        :return:
        """

        return tuple(sorted([str(method[0]) for method in self._ris.service]))

    @cucm_logging
    def axlAddCallPickupGroup(self, **kwargs: dict) -> dict:

        """
        AXL Add Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {
                                "callPickupGroup": {
                                    "name": "str",
                                    "pattern": "str"
                                }
                            }`
        :return:
        """

        return self._axl.addCallPickupGroup(**kwargs)

    @cucm_logging
    def axlAddDeviceProfile(self, **kwargs: dict) -> dict:

        """
        AXL Add Object Method.

        * product: `Cisco 7821`, `...`
        * class: `Phone`
        * protocol: `SIP`, `SCCP`
        * protocolSide: `User`
        * phoneTemplateName: `Standard 7821 SIP`, `...`

        :param kwargs:      Required Fields:
                            `kwargs = {
                                "deviceProfile": {
                                    "name": str,
                                    "product": "str",
                                    "class": "str",
                                    "protocol": "str",
                                    "protocolSide": "str",
                                    "phoneTemplateName": "str",
                                }
                            }`
        :return:
        """

        return self._axl.addDeviceProfile(**kwargs)

    @cucm_logging
    def axlAddLine(self, **kwargs: dict) -> dict:

        """
        AXL Add Object Method.

        * usage: `Device`

        :param kwargs:      Required Fields:
                            `kwargs = {
                                "line": {
                                    "pattern": "str",
                                    "usage": "str"
                                }
                            }`
        :return:
        """

        return self._axl.addLine(**kwargs)

    @cucm_logging
    def axlAddLineGroup(self, **kwargs: dict) -> dict:

        """
        AXL Add Object Method.

        * distributionAlgorithm: `Top Down`, `Circular`, `Longest Idle Time`, `Broadcast`
        * huntAlgorithmNoAnswer:
            `Try next member; then, try next group in Hunt List`,\n
            `Try next member, but do not go to next group`,\n
            `Skip remaining members, and go directly to next group`,\n
            `Stop hunting`
        * huntAlgorithmBusy:
            `Try next member; then, try next group in Hunt List`,\n
            `Try next member, but do not go to next group`,\n
            `Skip remaining members, and go directly to next group`,\n
            `Stop hunting`
        * huntAlgorithmNotAvailable:
            `Try next member; then, try next group in Hunt List`,\n
            `Try next member, but do not go to next group`,\n
            `Skip remaining members, and go directly to next group`,\n
            `Stop hunting`

        :param kwargs:      Required Fields:
                            `kwargs = {
                                "lineGroup": {
                                    "name": "str",
                                    "distributionAlgorithm": "str",
                                    "rnaReversionTimeOut": "int",
                                    "huntAlgorithmNoAnswer": "str",
                                    "huntAlgorithmBusy": "str",
                                    "huntAlgorithmNotAvailable": "str"
                                }
                            }`
        :return:
        """

        return self._axl.addLineGroup(**kwargs)

    @cucm_logging
    def axlAddPhone(self, **kwargs: dict) -> dict:

        """
        AXL Add Object Method.

        * product: `Cisco 7821`, `...`
        * class: `Phone`
        * protocol: `SIP`, `SCCP`
        * protocolSide: `User`
        * commonPhoneConfigName: `Standard Common Phone Profile`
        * locationName: `Hub_None`, `Phantom`, `Shadow`
        * useTrustedRelayPoint: `Default`, `On`, `Off`
        * phoneTemplateName: `Standard 7821 SIP`, `...`
        * primaryPhoneName: `None`
        * builtInBridgeStatus: `Default`, `On`, `Off`
        * packetCaptureMode: `None`, `Batch Processing Mode`
        * certificateOperation: `No Pending Operation`, `Install/Upgrade`, `Delete`, `Troubleshoot`
        * deviceMobilityMode: `Default`, `On`, `Off`

        :param kwargs:      Required Fields:
                            `kwargs = {
                                "phone": {
                                    "name",
                                    "product": "str",
                                    "class": "str",
                                    "protocol": "str",
                                    "protocolSide": "str",
                                    "devicePoolName": "str",
                                    "commonPhoneConfigName": "str",
                                    "locationName": "str",
                                    "useTrustedRelayPoint": "str",
                                    "phoneTemplateName": "str",
                                    "primaryPhoneName": None,
                                    "builtInBridgeStatus": "str",
                                    "packetCaptureMode": "str",
                                    "certificateOperation": "str",
                                    "deviceMobilityMode": "str"
                                }
                            }`
        :return:
        """

        return self._axl.addPhone(**kwargs)

    @cucm_logging
    def axlAddRemoteDestination(self, **kwargs: dict) -> dict:

        """
        AXL Add Object Method.

        * answerTooSoonTimer: `1500`
        * answerTooLateTimer: `19000`
        * delayBeforeRingingCell: `4000`

        :param kwargs:      Required Fields:
                            `kwargs = {
                                "remoteDestination": {
                                    "destination": "str",
                                    "answerTooSoonTimer": "int",
                                    "answerTooLateTimer": "int",
                                    "delayBeforeRingingCell": "int",
                                    "ownerUserId": "str",
                                    "remoteDestinationProfileName": "str"
                                }
                            }`
        :return:
        """

        # https://community.cisco.com/t5/cisco-bug-discussions/cscvq98025-addremotedestination-schema-requires/td-p/4305081
        # https://github.com/CiscoDevNet/axl-python-zeep-samples/blob/master/axl_add_Remote_Destination.py

        # Due to an issue with the AXL schema vs. implementation (11.5/12.5 - CSCvq98025)
        # we have to remove the nil <dualModeDeviceName> element Zeep creates
        # via the following lines

        # Use the Zeep service to create an XML object of the request - don't send
        req = self._axl_client.create_message(self._axl, "addRemoteDestination", **kwargs)
        for element in req.xpath("//dualModeDeviceName"):
            # Remove the dualModeDeviceName element
            element.getparent().remove(element)

        return self._axl_transport.post_xml(
            f"https://{self._cucm_publisher_property}:8443/axl/",
            envelope=req,
            headers=None
        )

    @cucm_logging
    def axlAddRemoteDestinationProfile(self, **kwargs: dict) -> dict:

        """
        AXL Add Object Method.

        * product: `Remote Destination Profile`
        * class: `Remote Destination Profile`
        * protocol: `Remote Destination`
        * protocolSide: `User`
        * callInfoPrivacyStatus: `Default`

        :param kwargs:      Required Fields:
                            `kwargs = {
                                "remoteDestinationProfile": {
                                    "name": "str",
                                    "product": "str",
                                    "class": "str",
                                    "protocol": "str",
                                    "protocolSide": "str",
                                    "devicePoolName": "str",
                                    "callInfoPrivacyStatus": "str",
                                    "userId": "str"
                                }
                            }`
        :return:
        """

        return self._axl.addRemoteDestinationProfile(**kwargs)

    @cucm_logging
    def axlAddTranslationPattern(self, **kwargs: dict) -> dict:

        """
        AXL Add Object Method.

        * usage: `Translation`

        :param kwargs:      Required Fields:
                            `kwargs = {
                                "transPattern": {
                                    "pattern": "str",
                                    "routePartitionName": "str",
                                    "usage": "str"
                                }
                            }`
        :return:
        """

        return self._axl.addTransPattern(**kwargs)

    @cucm_logging
    def axlAddUser(self, **kwargs: dict) -> dict:

        """
        AXL Add Object Method.

        * presenceGroupName: `Standard Presence group`

        :param kwargs:      Required Fields:
                            `kwargs = {
                                "user": {
                                    "userid": "str",
                                    "lastName": "str",
                                    "presenceGroupName": "str"
                                }
                            }`
        :return:
        """

        return self._axl.addUser(**kwargs)

    @cucm_logging
    def axlDoAuthenticateUser(self, **kwargs: Union[dict, ...]) -> dict:

        """
        AXL Do Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"userid": "str", "password": "str"}`
                            or
                            `kwargs = {"userid": "str", "pin": "str"}`
        :return:
        """

        return self._axl.doAuthenticateUser(**kwargs)

    @cucm_logging
    def axlDoDeviceLogin(self, **kwargs: Union[dict, ...]) -> dict:

        """
        AXL Do Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {
                                "deviceName": "str",
                                "loginDuration": "str",
                                "profileName": "str",
                                "userid": "str"
                            }`
        :return:
        """

        return self._axl.doDeviceLogin(**kwargs)

    @cucm_logging
    def axlDoDeviceLogout(self, **kwargs: Union[dict, ...]) -> dict:

        """
        AXL Do Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"deviceName": "str"}`
        :return:
        """

        return self._axl.doDeviceLogout(**kwargs)

    @cucm_logging
    def axlDoLdapSync(self, **kwargs: Union[dict, ...]) -> dict:

        """
        AXL Do Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID", "sync": "bool"}`
                            or
                            `kwargs = {"name": "str", "sync": "bool"}`
        :return:
        """

        return self._axl.doLdapSync(**kwargs)

    @cucm_logging
    def axlGetCallPickupGroup(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Get Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
                            or
                            `kwargs = {"pattern": "str"}`
                            or
                            `kwargs = {
                                "pattern": "str",
                                "routePartitionName": "str"
                            }`
        :return:
        """

        return serialize_object(self._axl.getCallPickupGroup(**kwargs)["return"]["callPickupGroup"], dict)

    @cucm_logging
    def axlGetDeviceProfile(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Get Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return serialize_object(self._axl.getDeviceProfile(**kwargs)["return"]["deviceProfile"], dict)

    @cucm_logging
    def axlGetLine(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Get Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"pattern": "str"}`
                            or
                            `kwargs = {
                                "pattern": "str",
                                "routePartitionName": "str"
                            }`
        :return:
        """

        return serialize_object(self._axl.getLine(**kwargs)["return"]["line"], dict)

    @cucm_logging
    def axlGetLineGroup(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Get Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return serialize_object(self._axl.getLineGroup(**kwargs)["return"]["lineGroup"], dict)

    @cucm_logging
    def axlGetPhone(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Get Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return serialize_object(self._axl.getPhone(**kwargs)["return"]["phone"], dict)

    @cucm_logging
    def axlGetRemoteDestination(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Get Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"destination": "str"}`
        :return:
        """

        return serialize_object(self._axl.getRemoteDestination(**kwargs)["return"]["remoteDestination"], dict)

    @cucm_logging
    def axlGetRemoteDestinationProfile(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Get Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return serialize_object(
            self._axl.getRemoteDestinationProfile(**kwargs)["return"]["remoteDestinationProfile"], dict)

    @cucm_logging
    def axlGetTranslationPattern(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Get Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"pattern": "str"}`
                            or
                            `kwargs = {
                                "pattern": "str",
                                "routePartitionName": "str"
                            }`
        :return:
        """

        return serialize_object(self._axl.getTransPattern(**kwargs)["return"]["transPattern"], dict)

    @cucm_logging
    def axlGetUser(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Get Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"userid": "str"}`
        :return:
        """

        return serialize_object(self._axl.getUser(**kwargs)["return"]["user"], dict)

    @cucm_logging
    def axlRemoveCallPickupGroup(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Remove Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
                            or
                            `kwargs = {"pattern": "str"}`
                            or
                            `kwargs = {
                                "pattern": "str",
                                "routePartitionName": "str"
                            }`
        :return:
        """

        return self._axl.removeCallPickupGroup(**kwargs)

    @cucm_logging
    def axlRemoveDeviceProfile(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Remove Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return self._axl.removeDeviceProfile(**kwargs)

    @cucm_logging
    def axlRemoveLine(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Remove Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"pattern": "str"}`
                            or
                            `kwargs = {
                                "pattern": "str",
                                "routePartitionName": "str"
                            }`
        :return:
        """

        return self._axl.removeLine(**kwargs)

    @cucm_logging
    def axlRemoveLineGroup(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Remove Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return self._axl.removeLineGroup(**kwargs)

    @cucm_logging
    def axlRemovePhone(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Remove Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return self._axl.removePhone(**kwargs)

    @cucm_logging
    def axlRemoveRemoteDestination(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Remove Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"destination": "str"}`
        :return:
        """

        return self._axl.removeRemoteDestination(**kwargs)

    @cucm_logging
    def axlRemoveRemoteDestinationProfile(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Remove Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return self._axl.removeRemoteDestinationProfile(**kwargs)

    @cucm_logging
    def axlRemoveTranslationPattern(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Remove Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"pattern": "str"}`
                            or
                            `kwargs = {
                                "pattern": "str",
                                "routePartitionName": "str"
                            }`
        :return:
        """

        return self._axl.removeTransPattern(**kwargs)

    @cucm_logging
    def axlRemoveUser(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Remove Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"userid": "str"}`
        :return:
        """

        return self._axl.removeUser(**kwargs)

    @cucm_logging
    def axlResetPhone(self, **kwargs: Union[dict, ...]) -> dict:

        """
        AXL Reset Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return self._axl.resetPhone(**kwargs)

    @cucm_logging
    def axlRestartPhone(self, **kwargs: Union[dict, ...]) -> dict:

        """
        AXL Restart Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return self._axl.restartPhone(**kwargs)

    @cucm_logging
    def axlUpdateCallPickupGroup(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Update Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
                            or
                            `kwargs = {"pattern": "str"}`
                            or
                            `kwargs = {
                                "pattern": "str",
                                "routePartitionName": "str"
                            }`
        :return:
        """

        return self._axl.updateCallPickupGroup(**kwargs)

    @cucm_logging
    def axlUpdateDeviceProfile(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Update Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return self._axl.updateDeviceProfile(**kwargs)

    @cucm_logging
    def axlUpdateLine(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Update Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"pattern": "str"}`
                            or
                            `kwargs = {
                                "pattern": "str",
                                "routePartitionName": "str"
                            }`
        :return:
        """

        return self._axl.updateLine(**kwargs)

    @cucm_logging
    def axlUpdateLineGroup(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Update Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return self._axl.updateLineGroup(**kwargs)

    @cucm_logging
    def axlUpdatePhone(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Update Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return self._axl.updatePhone(**kwargs)

    @cucm_logging
    def axlUpdateRemoteDestination(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Update Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"destination": "str"}`
        :return:
        """

        return self._axl.updateRemoteDestination(**kwargs)

    @cucm_logging
    def axlUpdateRemoteDestinationProfile(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Update Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return self._axl.updateRemoteDestinationProfile(**kwargs)

    @cucm_logging
    def axlUpdateTranslationPattern(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Update Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"pattern": "str"}`
                            or
                            `kwargs = {
                                "pattern": "str",
                                "routePartitionName": "str"
                            }`
        :return:
        """

        return self._axl.updateTransPattern(**kwargs)

    @cucm_logging
    def axlUpdateUser(self, **kwargs: Union[dict, ...]) -> Optional[Dict[str, Any]]:

        """
        AXL Update Object Method.
        :param kwargs:      Required Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"userid": "str"}`
        :return:
        """

        return self._axl.updateUser(**kwargs)

    @cucm_logging
    def ccsDoControlServices(self, control_command: str, service_names: list, node_fqdn: str = None):

        """
        CCS (Control Center Services) Do Control Services Method.
        :param control_command: Service(s) Control Command: `Restart`, `Start` or `Stop`
        :param service_names:   Service Names Collection
        :param node_fqdn:       Cluster Node FQDN or IP Address, Return Status From the Pub If the Node isn't Specified
        :return:
        """

        client = self._cucm_ccs_custom_node_service(node_fqdn=node_fqdn)
        validated_data = CucmCcsDoControlModel(**{
            # "NodeName": node_fqdn,        # Do not work properly
            "ControlType": control_command,
            "ServiceList": {"item": service_names}
        }).model_dump()
        return tuple(
            serialize_object(client.soapDoControlServices(validated_data), dict)["ServiceInfoList"]["item"]
        )

    @cucm_logging
    def ccsDoServiceDeployment(self, deploy_command: str, service_names: list, node_fqdn: str = None) -> tuple[dict]:

        """
        CCS (Control Center Services) Do Service Deployment Method.
        :param deploy_command:  Service(s) Deploy Command: `Deploy` or `UnDeploy`
        :param service_names:   Service Names Collection
        :param node_fqdn:       Cluster Node FQDN or IP Address, Return Status From the Pub If the Node isn't Specified
        :return:
        """

        client = self._cucm_ccs_custom_node_service(node_fqdn=node_fqdn)
        validated_data = CucmCcsDoDeploymentModel(**{
            # "NodeName": node_fqdn,        # Do not work properly
            "DeployType": deploy_command,
            "ServiceList": {"item": service_names}
        }).model_dump()
        return tuple(
            serialize_object(client.soapDoServiceDeployment(validated_data), dict)["ServiceInfoList"]["item"]
        )

    @cucm_logging
    def ccsGetProductInfoList(self, node_fqdn: str = None) -> tuple[dict]:

        """
        CCS (Control Center Services) Get Product Information Method.
        :param node_fqdn:       Cluster Node FQDN or IP Address, Return Status From the Pub If the Node isn't Specified
        :return:
        """

        client = self._cucm_ccs_custom_node_service(node_fqdn=node_fqdn)
        return client.getProductInformationList("")

    @cucm_logging
    def ccsGetServiceStatus(self, service_name: str = "", node_fqdn: str = None) -> tuple[dict]:

        """
        CCS (Control Center Services) Get Service Status Method.
        :param service_name:    Service Name, Return All Services if None
        :param node_fqdn:       Cluster Node FQDN or IP Address, Return Status From the Pub If the Node isn't Specified
        :return:
        """

        client = self._cucm_ccs_custom_node_service(node_fqdn=node_fqdn)
        return tuple(
            serialize_object(client.soapGetServiceStatus(service_name), dict)["ServiceInfoList"]["item"]
        )

    @cucm_logging
    def ccsGetStaticServiceList(self, node_fqdn: str = None) -> tuple[dict]:

        """
        CCS (Control Center Services) Get Static Service Method.
        :param node_fqdn:       Cluster Node FQDN or IP Address, Return Status From the Pub If the Node isn't Specified
        :return:
        """

        client = self._cucm_ccs_custom_node_service(node_fqdn=node_fqdn)
        return tuple(serialize_object(client.soapGetStaticServiceList(""), dict)["item"])

    @cucm_logging
    def risGetCti(self, **kwargs: Union[dict, ...]) -> dict:

        """
        RIS (Real-time Information Server) Get CTI Method.

        * collection_name: `DevNames`, `DirNumbers`
        * items_collection: Collection of Dictionaries. Depending on the type of collection, dictionaries should
          contain the key `name` for `DevNames` or the key `pattern` for `DirNumbers`
        * cti_mgr_class: `Provider`, `Device`, `Line`

        :param kwargs:  Required Fields:
                        `kwargs = {
                            "collection_name": "Enum",
                            "items_collection": "Iterable",
                            "cti_mgr_class": "Enum"
                        }`
        :return:
        """

        validated_data = CucmRisGetCtiModel(**kwargs).model_dump()

        state_info = ""
        criteria = {
            "MaxReturnedItems": 1000,
            "CtiMgrClass": validated_data["cti_mgr_class"].value,
            "Status": "Any",
            "NodeName": None,
            "SelectAppBy": "AppId",
            "AppItems": {"item": []},
            "DevNames": {"item": []},
            "DirNumbers": {"item": []},
            validated_data["collection_name"]: {"item": validated_data["items_collection"]}
        }
        return self._ris.service.selectCtiItem(state_info, self._ris_factory.CtiSelectionCriteria(**criteria))

    @cucm_logging
    def risGetPhone(self, phone_name: str, is_raw_resp: bool = False) -> dict:

        """
        RIS (Real-time Information Server) Get Phone Method.
        :param phone_name:  Phone Name
        :param is_raw_resp: Raw or Short Dictionary Response
        :return:
        """

        state_info = ""
        criteria = self._ris_factory.CmSelectionCriteria(
            MaxReturnedDevices=1,
            DeviceClass="Phone",
            Model=255,
            Status="Any",
            NodeName=None,
            SelectBy="Name",
            SelectItems={"item": [{"Item": phone_name}]},
            Protocol="Any",
            DownloadStatus="Any"
        )
        resp_raw = self._ris.service.selectCmDeviceExt(state_info, criteria)
        if is_raw_resp:
            return resp_raw
        return self.__cucm_ris_phone_resp_normalizing(resp_raw=resp_raw)[0]

    @cucm_logging
    def risGetPhones(self, devices_collection: Iterable[dict, ...], is_raw_resp: bool = False) -> tuple[dict, ...]:

        """
        RIS (Real-time Information Server) Get Phones Method.
        :param devices_collection:  Collection of Dictionaries. Dictionaries should contain the key `name`
        :param is_raw_resp:         Raw or Short Dictionary Response
        :return:
        """

        state_info = ""

        # Split collection
        splitted_devices_collection = [
            {"item": [{"Item": device["name"]} for device in devices_collection[item:item + 1000]]}
            for item in range(0, len(devices_collection), 1000)
        ]

        resp_raw_collection = []
        temp_norm_collection = {}
        for devices_collection_part in splitted_devices_collection:
            # Max Returned Devices Limit = 1000
            criteria = self._ris_factory.CmSelectionCriteria(
                MaxReturnedDevices=1000,
                DeviceClass="Phone",
                Model=255,
                Status="Any",
                NodeName=None,
                SelectBy="Name",
                SelectItems=devices_collection_part,
                Protocol="Any",
                DownloadStatus="Any"
            )
            resp_raw = self._ris.service.selectCmDeviceExt(state_info, criteria)
            if is_raw_resp:
                resp_raw_collection.append(resp_raw)
            else:
                for item in self.__cucm_ris_phone_resp_normalizing(resp_raw=resp_raw):
                    temp_norm_collection[item["DeviceName"]] = item

        if is_raw_resp:
            return tuple(resp_raw_collection)
        for device in devices_collection:
            if device["name"] in temp_norm_collection:
                device["ris"] = temp_norm_collection[device["name"]]
            else:
                # Device not found (Not exist, Off-line, Unsupported Class or Type (RDP, UDP and ect.))
                device["ris"] = {
                    "DeviceName": None,
                    "Status": None,
                    "Model": None,
                    "Product": None,
                    "IP": None,
                    "NodeName": None,
                    "ActiveLoadID": None,
                    "InactiveLoadID": None,
                }
        return tuple(devices_collection)

    @cucm_logging
    def sqlUpdateQuery(self, sql_query: str):

        """
        SQL Update Request to the Cisco UCM DB Informix.
        :param sql_query:   SQL `UPDATE` Query Expression
        :return:
        """

        return self._axl.executeSQLUpdate(sql=sql_query)

    def sqlExecuteQuery(self, sql_query: str) -> Union[tuple[dict, ...], None]:

        """
        SQL Select Request to the Cisco UCM DB Informix.
        :param sql_query:   SQL `SELECT` Query Expression
        :return:
        """

        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlGetDeviceEndUsersRelations(self, obj: Union[str, UUID]) -> Union[tuple[dict, ...], None]:

        """
        SQL Get Object Method.
        :param obj:     Object PKID or Name
        :return:
        """

        # One Device - A lot of End Users or None End Users
        sql_query = """SELECT eu.pkid AS enduser_pkid,
                              eu.userid,
                              eu.displayname AS enduser_displayname,
                              d.pkid AS device_pkid,
                              d.name AS device,
                              d.description AS device_description,
                              tc.name AS device_class,
                              tp.name AS device_product,
                              np.dnorpattern AS line,
                              rp.name AS line_partition,
                              np.description AS line_description
                         FROM enduser eu
                    LEFT JOIN enduserdevicemap eudm ON eudm.fkenduser = eu.pkid
                    LEFT JOIN device d ON d.pkid = eudm.fkdevice
                    LEFT JOIN devicenumplanmap dnpm ON dnpm.fkdevice = d.pkid
                    LEFT JOIN numplan np ON np.pkid = dnpm.fknumplan
                    LEFT JOIN routepartition rp ON rp.pkid = np.fkroutepartition
                    LEFT JOIN typeclass tc ON tc.enum = d.tkclass
                    LEFT JOIN typeproduct tp ON tp.enum = d.tkproduct
                        WHERE d.pkid = '{val}'
                           OR LOWER(d.name) = '{val}'
                     ORDER BY eu.userid""".format(val=str(obj).lower() if isinstance(obj, UUID) else obj.lower()
        )
        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlGetDeviceServicesSubscription(self, obj: Union[str, UUID]) -> Union[tuple[dict, ...], None]:

        """
        SQL Get Object Method.
        :param obj:     Object PKID or Name
        :return:
        """

        # One Device - A lot of Services or None Services
        sql_query = """SELECT d.name,
                              d.description,  
                              d.allowhotelingflag AS em_enable,
                              tss.servicename AS service_name
                         FROM device d 
                    LEFT JOIN telecastersubscribedservice tss on tss.fkdevice = d.pkid
                        WHERE d.pkid = '{val}'
                           OR LOWER(d.name) = '{val}'
                     ORDER BY d.name, tss.servicename""".format(
            val=str(obj).lower() if isinstance(obj, UUID) else obj.lower()
        )
        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlGetEMSession(self, obj: Union[str, UUID]) -> Optional[Dict[str, Any]]:

        """
        SQL Get Object Method.
        :param obj:     Object PKID or Name
        :return:
        """

        sql_query = """SELECT d.pkid,
                              d.name,
                              d.description,
                              d.allowhotelingflag AS em_enabled,
                              tm.name AS model,
                              emd.logintime AS login_time,
                              emd.loginduration AS login_duration,
                              emd.datetimestamp,
                              udp.pkid AS device_profile_pkid,
                              udp.name AS device_profile,
                              udp.description AS device_profile_description,
                              eu.userid,
                              eu.displayname AS display_name,
                              eul.userid AS userid_last,
                              eul.displayname AS display_name_last
                         FROM extensionmobilitydynamic emd
                    LEFT JOIN device d ON emd.fkdevice = d.pkid
                    LEFT JOIN device udp ON  emd.fkdevice_currentloginprofile = udp.pkid
                    LEFT JOIN typemodel tm ON d.tkmodel=tm.enum
                    LEFT JOIN enduser eu ON emd.fkenduser = eu.pkid
                    LEFT JOIN enduser eul ON emd.fkenduser_lastlogin = eul.pkid
                        WHERE d.pkid = '{val}'
                           OR LOWER(d.name) = '{val}'""".format(
            val=str(obj).lower() if isinstance(obj, UUID) else obj.lower()
        )
        resp_result = self.sqlExecuteQuery(sql_query=sql_query)
        if resp_result:
            resp_result = resp_result[0]
            if resp_result["login_time"]:
                resp_result["login_time"] = int(resp_result["login_time"])
                auto_logout = resp_result["login_time"] + int(resp_result["login_duration"])

                # Local Time Zone
                resp_result["auto_logout"] = datetime.fromtimestamp(auto_logout).isoformat()
                resp_result["login_time"] = datetime.fromtimestamp(resp_result["login_time"]).isoformat()
        # 'resp_result' is None if device doesn't exist or extension mobility is disabled.
        return resp_result

    def sqlGetEndUserDefaultDeviceProfile(self, obj: Union[str, UUID]) -> Optional[Dict[str, Any]]:

        """
        SQL Get Object Method.
        :param obj:    Object PKID or UserID
        :return:
        """

        # 'tkuserassociation' (Association Type):
        # 1 - Controlled Devices (Phones & SoftPhones)
        # 5 - Controlled User Device Profiles
        # 7 - CTI Controlled Device Profiles
        sql_query = """SELECT eu.pkid,
                              eu.userid,
                              eu.displayname AS display_name,
                              d.name AS device_profile,
                              eudm.tkuserassociation AS association_type,
                              eudm.defaultprofile AS is_default_udp
                         FROM enduser eu
                    LEFT JOIN enduserdevicemap eudm ON eu.pkid = eudm.fkenduser
                    LEFT JOIN device d ON eudm.fkdevice = d.pkid
                        WHERE (eu.pkid = '{val}' OR LOWER(eu.userid) = '{val}')
                          AND eudm.tkuserassociation = '5'
                          AND eudm.defaultprofile = 't'""".format(
            val=str(obj).lower() if isinstance(obj, UUID) else obj.lower()
        )
        resp_result = self.__cucm_sql_execute(sql_query=sql_query)
        if resp_result:
            resp_result = resp_result[0]
        return resp_result

    def sqlGetEndUserDevicesRelations(self, obj: Union[str, UUID]) -> Union[tuple[dict, ...], None]:

        """
        SQL Get Object Method.
        :param obj:    Object PKID or UserID
        :return:
        """

        # One End User - A lot of Devices or None Devices
        sql_query = """SELECT eu.pkid AS enduser_pkid,
                              eu.userid,
                              eu.displayname AS enduser_displayname,
                              d.pkid AS device_pkid,
                              d.name AS device,
                              d.description AS device_description,
                              tc.name AS device_class,
                              tp.name AS device_product,
                              np.dnorpattern AS line,
                              rp.name AS line_partition,
                              np.description AS line_description
                         FROM enduser eu
                    LEFT JOIN enduserdevicemap eudm ON eudm.fkenduser = eu.pkid
                    LEFT JOIN device d ON d.pkid = eudm.fkdevice
                    LEFT JOIN devicenumplanmap dnpm ON dnpm.fkdevice = d.pkid
                    LEFT JOIN numplan np ON np.pkid = dnpm.fknumplan
                    LEFT JOIN routepartition rp ON rp.pkid = np.fkroutepartition
                    LEFT JOIN typeclass tc ON tc.enum = d.tkclass
                    LEFT JOIN typeproduct tp ON tp.enum = d.tkproduct
                        WHERE eu.pkid = '{val}'
                           OR LOWER(eu.userid) = '{val}'
                     ORDER BY d.name""".format(val=str(obj).lower() if isinstance(obj, UUID) else obj.lower())
        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlGetLineGroupStatus(self, obj: Union[str, UUID]) -> Optional[Dict[str, Any]]:

        """
        SQL Get Object Method.
        :param obj:    Object PKID or Name
        :return:

        Optional:
        dnpm.numplanindex AS device_order
        """

        sql_query = """SELECT lgmap.lineselectionorder AS member_index,
                              np.dnorpattern AS member_line,
                              rp.name AS member_partition,
                              np.description AS member_description,
                              dhd.hlog AS status,
                              d.name AS device,
                              d.description AS device_description,
                              'phone' AS usage
                         FROM linegroup lg
                         JOIN linegroupnumplanmap lgmap ON lgmap.fklinegroup = lg.pkid
                         JOIN numplan np ON lgmap.fknumplan = np.pkid
                         JOIN routepartition rp ON np.fkroutepartition = rp.pkid
                         JOIN devicenumplanmap dmap ON dmap.fknumplan = np.pkid
                         JOIN device d ON dmap.fkdevice = d.pkid
                    LEFT JOIN extensionmobilitydynamic emd ON emd.fkdevice_currentloginprofile = dmap.pkid
                    LEFT JOIN device dp ON emd.fkdevice_currentloginprofile = dp.pkid
                         JOIN devicehlogdynamic dhd ON dhd.fkdevice = d.pkid
                        WHERE lg.pkid = '{val}'
                           OR LOWER(lg.name) = '{val}'
                 UNION SELECT lgmap.lineselectionorder AS member_index,
                              np.dnorpattern AS member_line,
                              rp.name AS member_partition,
                              np.description AS member_description,
                              dhd.hlog AS status,
                              d.name AS device,
                              d.description AS device_description,
                              'udp' AS usage
                         FROM extensionmobilitydynamic emd
                    LEFT JOIN device d ON d.pkid = emd.fkdevice
                         JOIN devicenumplanmap dnpm ON dnpm.fkdevice = emd.fkdevice_currentloginprofile
                         JOIN numplan np ON np.pkid = dnpm.fknumplan
                         JOIN routepartition rp ON np.fkroutepartition = rp.pkid
                         JOIN linegroupnumplanmap lgmap ON lgmap.fknumplan = np.pkid
                         JOIN linegroup lg ON lg.pkid = lgmap.fklinegroup
                    LEFT JOIN devicehlogdynamic dhd ON d.pkid = dhd.fkdevice
                        WHERE lg.pkid = '{val}'
                           OR LOWER(lg.name) = '{val}'
                     ORDER BY lgmap.lineselectionorder, d.name""".format(
            val=str(obj).lower() if isinstance(obj, UUID) else obj.lower()
        )
        resp_result = self.sqlExecuteQuery(sql_query=sql_query)
        if resp_result:
            for item in resp_result:
                item["status"] = "On-Line" if item["status"] == "t" else "Off-Line"
        return resp_result

    def sqlGetRemoteDestination(self, obj: Union[str, UUID]) -> Union[tuple[dict, ...], None]:

        """
        SQL Get Object Method.
        :param obj:    Object PKID or Name
        :return:
        """

        # Get Remote Destination via Remote Destination Profile
        sql_query = """SELECT rd.pkid,
                              rd.name,
                              rdd.destination,
                              rdd.enablesinglenumberreach AS snr,
                              rdd.ismobilephone AS is_mobile,
                              rdd.delaybeforeringingcell AS start_delay,
                              rdd.answertoolatetimer AS stop_ringing
                         FROM device d
                    LEFT JOIN remotedestination rd ON rd.fkdevice_remotedestinationtemplate = d.pkid
                    LEFT JOIN remotedestinationdynamic rdd ON rdd.fkremotedestination = rd.pkid
                        WHERE d.pkid = '{val}'
                           OR LOWER(d.name) = '{val}'
                     ORDER BY rd.name""".format(val=str(obj).lower() if isinstance(obj, UUID) else obj.lower())
        return self.sqlExecuteQuery(sql_query=sql_query)

    def sqlGetUnassignedPattern(self, pattern: str, patternusage: str, partition: str) -> Optional[Dict[str, Any]]:

        """
        SQL Get Object Method.
        :param pattern:         Pattern Value
        :param patternusage:    Pattern Usage Type
        :param partition:       Route Partition Name
        :return:
        """

        # No Device & Line Group Mapping
        sql_query = """SELECT np.pkid AS line_pkid, 
                              np.dnorpattern AS line,
                              rp.name AS line_partition
                         FROM numplan np
                    LEFT JOIN routepartition rp ON np.fkroutepartition = rp.pkid
                    LEFT JOIN devicenumplanmap dnmp ON dnmp.fknumplan = np.pkid
                    LEFT JOIN linegroupnumplanmap lgnmp ON lgnmp.fknumplan = np.pkid
                        WHERE dnmp.pkid IS NULL
                          AND lgnmp.pkid IS NULL
                          AND np.dnorpattern LIKE '{pattern}%'
                          AND np.tkpatternusage = '{patternusage}'
                          AND rp.name = '{partition}'
                     ORDER BY np.dnorpattern
        """.format(pattern=pattern, patternusage=patternusage, partition=partition)
        resp_result = self.sqlExecuteQuery(sql_query=sql_query)
        if resp_result:
            resp_result = choice(resp_result)
        return resp_result

    def sqlListCallingSearchSpace(self) -> Optional[Tuple[Dict[str, Any]]]:

        """
        SQL List Object(s) Method.
        :return:
        """

        return self.__cucm_sql_execute(
            sql_query="SELECT css.pkid, css.name, css.description FROM callingsearchspace css ORDER BY css.name"
        )

    def sqlListCredentialPolicy(self) -> Tuple[Dict[str, Any]]:

        """
        SQL List Object(s) Method.
        :return:
        """

        return self.__cucm_sql_execute(
            sql_query="SELECT cp.pkid, cp.displayname AS name FROM credentialpolicy cp ORDER BY cp.displayname"
        )

    def sqlListDevicePool(self) -> Tuple[Dict[str, Any]]:

        """
        SQL List Object(s) Method.
        :return:
        """

        return self.__cucm_sql_execute(sql_query="SELECT dp.pkid, dp.name FROM devicepool dp ORDER BY dp.name")

    def sqlListDirGroup(self) -> Tuple[Dict[str, Any]]:

        """
        SQL List Object(s) Method.
        :return:
        """

        return self.__cucm_sql_execute(sql_query="SELECT dg.pkid, dg.name FROM dirgroup dg ORDER BY dg.name")

    def sqlListMediaResourceGroup(self) -> Optional[Tuple[Dict[str, Any]]]:

        """
        SQL List Object(s) Method.
        :return:
        """

        return self.__cucm_sql_execute(
            sql_query="SELECT mrg.pkid, mrg.name, mrg.description FROM mediaresourcegroup mrg ORDER BY mrg.name"
        )

    def sqlListMediaResourceList(self) -> Optional[Tuple[Dict[str, Any]]]:

        """
        SQL List Object(s) Method.
        :return:
        """

        return self.__cucm_sql_execute(
            sql_query="SELECT mrl.pkid, mrl.name FROM mediaresourcelist mrl ORDER BY mrl.name"
        )

    def sqlListPhoneTemplate(self) -> Tuple[Dict[str, Any]]:

        """
        SQL List Object(s) Method.
        :return:
        """

        return self.__cucm_sql_execute(sql_query="SELECT pt.pkid, pt.name FROM phonetemplate pt ORDER BY pt.name")

    def sqlListProcessNode(self) -> Tuple[Dict[str, Any]]:

        """
        SQL List Object(s) Method.
        :return:
        """

        return self.__cucm_sql_execute(
            sql_query="""
                SELECT pn.pkid, pn.name, pn.description 
                FROM processnode pn 
                WHERE pn.name NOT LIKE 'EnterpriseWideData'
                ORDER BY pn.name
            """)

    def sqlListRecordingProfile(self) -> Optional[Tuple[Dict[str, Any]]]:

        """
        SQL List Object(s) Method.
        :return:
        """

        return self.__cucm_sql_execute(sql_query="SELECT rp.pkid, rp.name FROM recordingprofile rp ORDER BY rp.name")

    def sqlListRegion(self) -> Tuple[Dict[str, Any]]:

        """
        SQL List Object(s) Method.
        :return:
        """

        return self.__cucm_sql_execute(sql_query="SELECT r.pkid, r.name FROM region r ORDER BY r.name")

    def sqlListRoutePartition(self) -> Tuple[Dict[str, Any]]:

        """
        SQL List Object(s) Method.
        :return:
        """

        return self.__cucm_sql_execute(
            sql_query="SELECT rp.pkid, rp.name, rp.description FROM routepartition rp ORDER BY rp.name"
        )

    def sqlListSoftkeyTemplate(self) ->Tuple[Dict[str, Any]]:

        """
        SQL List Object(s) Method.
        :return:
        """

        return self.__cucm_sql_execute(
            sql_query="SELECT skt.pkid, skt.name, skt.description FROM softkeytemplate skt ORDER BY skt.name"
        )

    def sqlListTelecasterService(self) -> Tuple[Dict[str, Any]]:

        """
        SQL List Object(s) Method.
        :return:
        """

        return self.__cucm_sql_execute(
            sql_query="SELECT ts.pkid, ts.name, ts.description FROM telecasterservice ts ORDER BY ts.name"
        )

    def sqlListTypeClass(self) -> Tuple[Dict[str, Any]]:

        """
        SQL List Object(s) Method.
        :return:
        """

        return self.__cucm_sql_execute(sql_query="SELECT tc.enum AS pkid, tc.name FROM typeclass tc ORDER BY tc.enum")

    def sqlListTypeCountry(self) -> Tuple[Dict[str, Any]]:

        """
        SQL List Object(s) Method.
        :return:
        """

        return self.__cucm_sql_execute(sql_query="SELECT tc.enum AS pkid, tc.name FROM typecountry tc ORDER BY tc.enum")

    def sqlListTypeModel(self) -> Tuple[Dict[str, Any]]:

        """
        SQL List Object(s) Method.
        :return:
        """

        return self.__cucm_sql_execute(sql_query="SELECT tm.enum AS pkid, tm.name FROM typemodel tm ORDER BY tm.enum")

    def sqlListTypeUserLocale(self) -> Tuple[Dict[str, Any]]:

        """
        SQL List Object(s) Method.
        :return:
        """

        return self.__cucm_sql_execute(
            sql_query="SELECT tul.enum AS pkid, tul.name, tul.nativename FROM typeuserlocale tul ORDER BY tul.enum"
        )

    def sqlListUcServiceProfile(self) -> Optional[Tuple[Dict[str, Any]]]:

        """
        SQL List Object(s) Method.
        :return:
        """

        return self.__cucm_sql_execute(
            sql_query="SELECT ucsp.pkid, ucsp.name, ucsp.description FROM ucserviceprofile ucsp ORDER BY ucsp.name"
        )

    def sqlListUcUserProfile(self) -> Tuple[Dict[str, Any]]:

        """
        SQL List Object(s) Method.
        :return:
        """

        return self.__cucm_sql_execute(
            sql_query="SELECT ucup.pkid, ucup.name, ucup.description FROM ucuserprofile ucup ORDER BY ucup.name"
        )

    def sqlSearchCallPickupGroup(
        self, **kwargs: Unpack[CucmSqlSearchCallPickupGroupModel]
    ) -> Optional[Tuple[Dict[str, Any]]]:

        """
        SQL Search Object Method.

        Kwargs:
            criterion (str): One of the supported filtering fields:
                - "Name"
                - "Description"
                - "Pattern"
                - "Member Line Number"
                - "Member Line Description"

            value (str | None): The value to filter by. Special behavior applies depending on the criterion.

        Behavior per criterion and value:

        | Criterion                 | Value = "" (empty string) | Value = None                                  |
        |---------------------------|---------------------------|-----------------------------------------------|
        | "Name"                    | Returns all records       | Returns none (field is required)              |
        | "Description"             | Returns all records       | Returns records without CPG description       |
        | "Pattern"                 | Returns all records       | Returns none (field is required)              |
        | "Member Line Number"      | Returns all records       | Returns records without members (empty group) |
        | "Member Line Description" | Returns all records       | Returns records without member description    |

        :param kwargs:
        :return:
        """

        validated_data = CucmSqlSearchCallPickupGroupModel(**kwargs)

        condition_for_none = "= ''"
        if validated_data.sql_criterion == "npm.dnorpattern":
            # Search Empty Call Pickup Groups
            condition_for_none = "IS NULL"

        sql_query = """SELECT cpg.pkid,
                              cpg.name,
                              npg.description,
                              npg.dnorpattern AS pattern,
                              rpg.name AS partition,
                              npm.pkid AS line_pkid,
                              npm.dnorpattern AS line,
                              rpm.name AS line_partition,
                              npm.description AS line_description
                         FROM pickupgroup cpg
                    LEFT JOIN numplan npg ON npg.pkid = cpg.fknumplan_pickup
                    LEFT JOIN routepartition rpg ON rpg.pkid = npg.fkroutepartition
                    LEFT JOIN pickupgrouplinemap pglm ON pglm.fkpickupgroup = cpg.pkid
                    LEFT JOIN numplan npm ON npm.pkid = pglm.fknumplan_line
                    LEFT JOIN routepartition rpm ON rpm.pkid = npm.fkroutepartition
                        WHERE LOWER({obj}) {val}
                          AND npg.tkpatternusage = '4'
                     ORDER BY cpg.name""".format(
            obj=validated_data.sql_criterion,
            val=condition_for_none if validated_data.value is None else f"LIKE '%{validated_data.value.lower()}%'"
        )
        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlSearchDevice(self, **kwargs: Unpack[CucmSqlSearchDeviceModel]) -> Optional[Tuple[Dict[str, Any]]]:

        """
        SQL Search Object Method.

        Kwargs:
            criterion (str): One of the supported filtering fields:
                - "Name"
                - "Description"
                - "Line Number"
                - "Line Description"
                - "Userid"
                - "Device Pool"
                - "Device Type"

            value (str | None): The value to filter by. Special behavior applies depending on the criterion.

        Behavior per criterion and value:

        | Criterion          | Value = "" (empty string)                 | Value = None                               |
        |--------------------|-------------------------------------------|--------------------------------------------|
        | "Name"             | Returns all records                       | Returns none (field is required)           |
        | "Description"      | Returns all records                       | Returns records without device description |
        | "Line Number"      | Returns all records with line             | Returns records without line               |
        | "Line Description" | Returns all records with line description | Returns records without line description   |
        | "Userid"           | Returns all records with owner            | Returns records without owner              |
        | "Device Pool"      | Returns all records with device pool      | Returns records without device pool        |
        | "Device Type"      | Returns all records                       | Returns none (field is required)           |

        :param kwargs:
        :return:
        """

        validated_data = CucmSqlSearchDeviceModel(**kwargs)

        condition_for_none = "= ''"
        if validated_data.sql_criterion in ("np.dnorpattern", "eu.userid", "dp.name"):
            # Search Device Without Line, Userid, Device Pool
            condition_for_none = "IS NULL"

        sql_query = """SELECT d.pkid,
                              d.name,
                              d.description,
                              dp.name AS device_pool,
                              np.pkid AS line_pkid,
                              np.dnorpattern AS line,
                              dnpm.numplanindex AS line_index,
                              rp.name AS line_partition,
                              np.description AS line_description,
                              tc.name AS class,
                              tm.name AS model,
                              eu.pkid AS end_user_pkid,
                              eu.userid, 
                              eu.displayname AS display_name,
                              eu_rdp.pkid AS end_user_rdp_pkid,
                              eu_rdp.userid AS userid_rdp,
                              eu_rdp.displayname AS display_name_rdp
                         FROM device d
                    LEFT JOIN devicenumplanmap dnpm ON dnpm.fkdevice = d.pkid
                    LEFT JOIN numplan np ON np.pkid = dnpm.fknumplan
                    LEFT JOIN routepartition rp ON rp.pkid = np.fkroutepartition
                    LEFT JOIN devicepool dp ON dp.pkid = d.fkdevicepool
                    LEFT JOIN typemodel tm ON tm.enum = d.tkmodel
                    LEFT JOIN typeclass tc ON tc.enum = d.tkclass
                    LEFT JOIN typeproduct tprod ON tprod.tkmodel = d.tkmodel
                    LEFT JOIN enduser eu ON eu.pkid = d.fkenduser
                    LEFT JOIN enduser eu_rdp ON eu_rdp.pkid = d.fkenduser_mobility
                        WHERE LOWER({obj}) {val}
                          AND (d.tkclass = '1' OR d.tkclass = '20' OR d.tkclass = '254')
                          AND d.name NOT LIKE 'ModelProfile%'
                     ORDER BY d.name, dnpm.numplanindex""".format(
            obj=validated_data.sql_criterion,
            val=condition_for_none if validated_data.value is None else f"LIKE '%{validated_data.value.lower()}%'"
        )
        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlSearchDirectoryNumber(
        self, **kwargs: Unpack[CucmSqlSearchDirectoryNumberModel]
    ) -> Optional[Tuple[Dict[str, Any]]]:

        """
        SQL Search Object Method.

        Kwargs:
            criterion (str): One of the supported filtering fields:
                - "Pattern"
                - "Description"
                - "Partition"
                - "Calling Search Space"
                - "Alerting Name"
                - "Alerting Name ASCII"

            value (str | None): The value to filter by. Special behavior applies depending on the criterion.

        Behavior per criterion and value:

        | Criterion              | Value = "" (empty string)                     | Value = None                                 |
        |------------------------|-----------------------------------------------|----------------------------------------------|
        | "Pattern"              | Returns all records                           | Returns none (field is required)             |
        | "Description"          | Returns all records                           | Returns records without line description     |
        | "Partition"            | Returns all records with partition            | Returns records without partition            |
        | "Calling Search Space" | Returns all records with calling search space | Returns records without calling search space |
        | "Alerting Name"        | Returns all records                           | Returns records without alerting name        |
        | "Alerting Name ASCII"  | Returns all records                           | Returns records without alerting name ascii  |

        :param kwargs:
        :return:
        """

        validated_data = CucmSqlSearchDirectoryNumberModel(**kwargs)

        condition_for_none = "= ''"
        if validated_data.sql_criterion in ("rp.name", "css.name"):
            # Search Device Without Partition, Calling Search Space
            condition_for_none = "IS NULL"

        sql_query = """SELECT np.pkid,
                              np.dnorpattern AS pattern,
                              np.description,
                              np.alertingname,
                              np.alertingnameascii,
                              rp.name AS partition,
                              css.name AS css
                         FROM numplan np
                    LEFT JOIN routepartition rp ON rp.pkid = np.fkroutepartition
                    LEFT JOIN callingsearchspace css ON css.pkid = np.fkcallingsearchspace_sharedlineappear
                        WHERE LOWER({obj}) {val}
                          AND np.tkpatternusage = '2'
                     ORDER BY np.dnorpattern""".format(
            obj=validated_data.sql_criterion,
            val=condition_for_none if validated_data.value is None else f"LIKE '%{validated_data.value.lower()}%'"
        )
        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlSearchEndUser(self, **kwargs: Unpack[CucmSqlSearchEndUserModel]) -> Optional[Tuple[Dict[str, Any]]]:

        """
        SQL Search Object Method.

        Kwargs:
            criterion (str): One of the supported filtering fields:
                - "Userid"
                - "Display Name"
                - "Last Name"
                - "First Name"
                - "Phone Number"
                - "Mobile Number"
                - "Email"
                - "Directory URI"

            value (str | None): The value to filter by. Special behavior applies depending on the criterion.

        Behavior per criterion and value:

        | Criterion       | Value = "" (empty string) | Value = None                          |
        |-----------------|---------------------------|---------------------------------------|
        | "Userid"        | Returns all records       | Returns none (field is required)      |
        | "Display Name"  | Returns all records       | Returns records without display name  |
        | "Last Name"     | Returns all records       | Returns none (field is required)      |
        | "First Name"    | Returns all records       | Returns records without first name    |
        | "Phone Number"  | Returns all records       | Returns records without phone number  |
        | "Mobile Number" | Returns all records       | Returns records without mobile number |
        | "Email"         | Returns all records       | Returns records without email         |
        | "Directory URI" | Returns all records       | Returns records without directory uri |

        :param kwargs:
        :return:
        """

        validated_data = CucmSqlSearchEndUserModel(**kwargs)

        sql_query = """SELECT eu.pkid,
                              eu.userid,
                              eu.displayname AS display_name,
                              eu.lastname AS last_name,
                              eu.telephonenumber AS phone_number,
                              eu.mobile AS mobile_number,
                              eu.mailid,
                              eu.department,
                              eu.title,
                              eu.fkdirectorypluginconfig AS user_type,
                              eu.status AS user_status
                         FROM enduser eu
                        WHERE LOWER({obj}) {val}
                     ORDER BY eu.userid""".format(
            obj=validated_data.sql_criterion,
            val="LIKE ''" if validated_data.value is None else f"LIKE '%{validated_data.value.lower()}%'"
        )
        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlSearchLineGroup(self, **kwargs: Unpack[CucmSqlSearchLineGroupModel]) -> Optional[Tuple[Dict[str, Any]]]:

        """
        SQL Search Object Method.

        * criterion: `Name`, `Member Line Number`, `Member Line Description`
        * value: Search Value String

        Kwargs:
            criterion (str): One of the supported filtering fields:
                - "Name"
                - "Member Line Number"
                - "Member Line Description"

            value (str | None): The value to filter by. Special behavior applies depending on the criterion.

        Behavior per criterion and value:

        | Criterion                 | Value = "" (empty string) | Value = None                                  |
        |---------------------------|---------------------------|-----------------------------------------------|
        | "Name"                    | Returns all records       | Returns none (field is required)              |
        | "Member Line Number"      | Returns all records       | Returns records without members (empty group) |
        | "Member Line Description" | Returns all records       | Returns records without member description    |

        :param kwargs:
        :return:
        """

        validated_data = CucmSqlSearchLineGroupModel(**kwargs)

        condition_for_none = "= ''"
        if validated_data.sql_criterion == "np.dnorpattern":
            # Search Empty Line Groups
            condition_for_none = "IS NULL"

        sql_query = """SELECT lg.pkid,
                              lg.name,
                              tda.name AS algorithm,
                              np.pkid AS line_pkid,
                              np.dnorpattern AS line,
                              rp.name AS line_partition,
                              np.description AS line_description,
                              lgnpm.lineselectionorder AS line_index
                         FROM linegroup lg
                    LEFT JOIN linegroupnumplanmap lgnpm ON lgnpm.fklinegroup = lg.pkid
                    LEFT JOIN typedistributealgorithm tda ON tda.enum = lg.tkdistributealgorithm
                    LEFT JOIN numplan np ON np.pkid = lgnpm.fknumplan
                    LEFT JOIN routepartition rp ON rp.pkid = np.fkroutepartition
                        WHERE LOWER({obj}) {val}
                     ORDER BY lg.name, lgnpm.lineselectionorder""".format(
            obj=validated_data.sql_criterion,
            val=condition_for_none if validated_data.value is None else f"LIKE '%{validated_data.value.lower()}%'"
        )
        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlSearchRemoteDestination(
        self, **kwargs: Unpack[CucmSqlSearchRemoteDestinationModel]
    ) -> Optional[Tuple[Dict[str, Any]]]:

        """
        SQL Search Object Method.

        Kwargs:
            criterion (str): One of the supported filtering fields:
                - "Name"
                - "Destination"

            value (str | None): The value to filter by. Special behavior applies depending on the criterion.

        Behavior per criterion and value:

        | Criterion     | Value = "" (empty string) | Value = None                     |
        |---------------|---------------------------|----------------------------------|
        | "Name"        | Returns all records       | Returns none (field is required) |
        | "Destination" | Returns all records       | Returns none (field is required) |

        :param kwargs:
        :return:
        """

        validated_data = CucmSqlSearchRemoteDestinationModel(**kwargs)

        sql_query = """SELECT rd.pkid,
                              rd.name,
                              rdd.destination,
                              rdd.enablesinglenumberreach AS snr,
                              rdd.ismobilephone AS is_mobile,
                              rdd.delaybeforeringingcell AS start_delay,
                              rdd.answertoolatetimer AS stop_ringing
                         FROM remotedestination rd
                    LEFT JOIN remotedestinationdynamic rdd ON rdd.fkremotedestination = rd.pkid
                        WHERE LOWER({obj}) {val}
                     ORDER BY rd.name""".format(
            obj=validated_data.sql_criterion,
            val="= ''" if validated_data.value is None else f"LIKE '%{validated_data.value.lower()}%'"
        )
        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlSearchTranslationPattern(
        self, **kwargs: Unpack[CucmSqlSearchTranslationPatternModel]
    ) -> Optional[Tuple[Dict[str, Any]]]:

        """
        SQL Search Object Method.

        Kwargs:
            criterion (str): One of the supported filtering fields:
                - "Pattern"
                - "Description"
                - "Partition"
                - "Calling Search Space"
                - "Called Party Transform Mask"
                - "Prefix Digits Out"

            value (str | None): The value to filter by. Special behavior applies depending on the criterion.

        Behavior per criterion and value:

        | Criterion                     | Value = "" (empty string)                     | Value = None                                        |
        |-------------------------------|-----------------------------------------------|-----------------------------------------------------|
        | "Pattern"                     | Returns all records                           | Returns records without pattern                     |
        | "Description"                 | Returns all records                           | Returns records without description                 |
        | "Partition"                   | Returns all records with partition            | Returns records without partition                   |
        | "Calling Search Space"        | Returns all records with calling search space | Returns records without calling search space        |
        | "Called Party Transform Mask" | Returns all records                           | Returns records without called party transform mask |
        | "Prefix Digits Out"           | Returns all records                           | Returns records without prefix digits out           |

        :param kwargs:
        :return:
        """

        validated_data = CucmSqlSearchTranslationPatternModel(**kwargs)

        condition_for_none = "= ''"
        if validated_data.sql_criterion in ("rp.name", "css.name"):
            # Search Device Without Partition, Calling Search Space
            condition_for_none = "IS NULL"

        sql_query = """SELECT np.pkid,
                              np.dnorpattern AS pattern,
                              np.description,
                              rp.name AS partition,
                              css.name AS css,
                              np.calledpartytransformationmask AS called_tmask,
                              np.prefixdigitsout AS called_prefix,
                              rc.name AS route_class,
                              np.blockenable AS block_enable
                         FROM numplan np
                    LEFT JOIN routepartition rp ON rp.pkid = np.fkroutepartition
                    LEFT JOIN callingsearchspace css ON css.pkid = np.fkcallingsearchspace_translation
                    LEFT JOIN typepatternrouteclass rc ON rc.enum = np.tkpatternrouteclass
                        WHERE LOWER({obj}) {val}
                          AND np.tkpatternusage = '3'
                     ORDER BY np.dnorpattern""".format(
            obj=validated_data.sql_criterion,
            val=condition_for_none if validated_data.value is None else f"LIKE '%{validated_data.value.lower()}%'"
        )
        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlSearchUnassignedNumber(self, **kwargs: Unpack[CucmSqlSearchDirectoryNumberModel]):

        """
        SQL Search Object Method.

        Kwargs:
            criterion (str): One of the supported filtering fields:
                - "Pattern"
                - "Description"
                - "Partition"
                - "Calling Search Space"
                - "Alerting Name"
                - "Alerting Name ASCII"

            value (str | None): The value to filter by. Special behavior applies depending on the criterion.

        Behavior per criterion and value:

        | Criterion              | Value = "" (empty string)                     | Value = None                                 |
        |------------------------|-----------------------------------------------|----------------------------------------------|
        | "Pattern"              | Returns all records                           | Returns none (field is required)             |
        | "Description"          | Returns all records                           | Returns records without line description     |
        | "Partition"            | Returns all records with partition            | Returns records without partition            |
        | "Calling Search Space" | Returns all records with calling search space | Returns records without calling search space |
        | "Alerting Name"        | Returns all records                           | Returns records without alerting name        |
        | "Alerting Name ASCII"  | Returns all records                           | Returns records without alerting name ascii  |

        :param kwargs:
        :return:
        """

        validated_data = CucmSqlSearchDirectoryNumberModel(**kwargs)

        condition_for_none = "= ''"
        if validated_data.sql_criterion in ("rp.name", "css.name"):
            # Search Device Without Partition, Calling Search Space
            condition_for_none = "IS NULL"

        sql_query = """SELECT np.pkid,
                              np.dnorpattern AS pattern,
                              np.description,
                              np.alertingname,
                              np.alertingnameascii,
                              rp.name AS partition,
                              css.name AS css
                         FROM numplan np
                    LEFT JOIN routepartition rp ON np.fkroutepartition = rp.pkid
                    LEFT JOIN callingsearchspace css ON css.pkid = np.fkcallingsearchspace_sharedlineappear
                    LEFT JOIN devicenumplanmap dnmp ON dnmp.fknumplan = np.pkid
                    LEFT JOIN linegroupnumplanmap lgnmp ON lgnmp.fknumplan = np.pkid
                        WHERE dnmp.pkid IS NULL
                          AND lgnmp.pkid IS NULL
                          AND LOWER({obj}) {val}
                          AND np.tkpatternusage = '2'
                     ORDER BY np.dnorpattern""".format(
            obj=validated_data.sql_criterion,
            val=condition_for_none if validated_data.value is None else f"LIKE '%{validated_data.value.lower()}%'"
        )
        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlValidateEndUser(self, userid: str) -> Optional[Tuple[Dict[str, Any]]]:

        """
        SQL Validate Object Method.
        :param userid:      EndUserID
        :return:
        """

        sql_query = """SELECT eu.pkid AS enduser_pkid,
                              eu.userid,
                              eu.displayname AS enduser_displayname
                         FROM enduser eu
                        WHERE LOWER(eu.userid) = '{val}'
                          AND eu.status = '1'
                     ORDER BY eu.userid""".format(val=userid.lower())
        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlValidateLine(self, pattern: str) -> Optional[Tuple[Dict[str, Any]]]:

        """
        SQL Validate Object Method.
        :param pattern:     Pattern (`tkpatternusage = '2'` - Type Pattern Usage: Device Only)
        :return:
        """

        sql_query = """SELECT np.pkid AS line_pkid,
                              np.dnorpattern AS line,
                              np.description AS line_description,
                              rp.name AS line_partition
                         FROM numplan np
                    LEFT JOIN routepartition rp ON rp.pkid = np.fkroutepartition
                        WHERE LOWER(np.dnorpattern) = '{val}'
                          AND np.tkpatternusage = '2' 
                     ORDER BY np.dnorpattern""".format(val=pattern.lower())
        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlValidateLineDevices(self, pattern: str) -> Optional[Tuple[Dict[str, Any]]]:

        """
        SQL Validate Object Method.
        :param pattern:     Pattern (`tkpatternusage = '2'` - Type Pattern Usage: Device Only)
        :return:
        """

        sql_query = """SELECT d.pkid AS device_pkid,
                              d.name AS device,
                              d.description AS device_description,
                              tc.name AS device_class,
                              tm.name AS device_model,
                              np.pkid AS line_pkid,
                              np.dnorpattern AS line,
                              np.description AS line_description,
                              rp.name AS line_partition,
                              np.tkpatternusage AS pattern_usage,
                              tpu.name AS pattern_type
                         FROM device d
                    LEFT JOIN devicenumplanmap dnpm ON dnpm.fkdevice = d.pkid
                    LEFT JOIN numplan np ON np.pkid = dnpm.fknumplan
                    LEFT JOIN routepartition rp ON rp.pkid = np.fkroutepartition
                    LEFT JOIN typepatternusage tpu ON tpu.enum = np.tkpatternusage
                    LEFT JOIN typeclass tc ON tc.enum = d.tkclass
                    LEFT JOIN typemodel tm ON tm.enum = d.tkmodel
                        WHERE LOWER(np.dnorpattern) = '{val}'
                          AND np.tkpatternusage = '2' 
                          AND (d.tkclass = '1' OR d.tkclass = '20' OR d.tkclass = '254')
                          AND d.name NOT LIKE 'ModelProfile%'
                     ORDER BY d.name""".format(val=pattern.lower())
        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlValidatePattern(self, pattern: str) -> Optional[Tuple[Dict[str, Any]]]:

        """
        SQL Validate Object Method.
        :param pattern:     Pattern (`tkpatternusage` - Not Define. Any Pattern Type Usage)
        :return:
        """

        sql_query = """SELECT np.pkid AS pattern_pkid,
                              np.dnorpattern AS pattern,
                              np.description AS pattern_description,
                              rp.name AS pattern_partition,
                              np.tkpatternusage AS pattern_usage,
                              tpu.name AS pattern_type
                         FROM numplan np
                    LEFT JOIN routepartition rp ON rp.pkid = np.fkroutepartition
                    LEFT JOIN typepatternusage tpu ON tpu.enum = np.tkpatternusage
                        WHERE LOWER(np.dnorpattern) = '{val}'
                     ORDER BY np.dnorpattern""".format(val=pattern.lower())
        return self.__cucm_sql_execute(sql_query=sql_query)
