from typing import Iterable, Union
from zeep.helpers import serialize_object
from .decorators import cucm_logging
from .settings import CucmSettings
from .sql_models import (
    CucmSqlSearchCallPickupGroupModel,
    CucmSqlSearchDeviceModel,
    CucmSqlSearchEndUserModel,
    CucmSqlSearchLineGroupModel,
    CucmSqlSearchTranslationPatternModel,
)


""" ######################################################### """
""" ******************** TINY CUCM CLIENT ******************* """
""" ######################################################### """


class CucmAxlClient(CucmSettings):

    """
        tinyCUCM AXL Client. Cisco Unified Call Manager AXL Methods Collection
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
    def axlAllMethods(self) -> Union[tuple[str, ...], None]:

        """
        AXL All Methods Collection.
        :return:
        """

        return tuple(sorted([str(method[0]) for method in self._axl]))

    @cucm_logging
    def axlDoAuthenticateUser(self, **kwargs: dict):

        """
        AXL Do Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"userid": "str", "password": "str"}`
                            or
                            `kwargs = {"userid": "str", "pin": "str"}`
        :return:
        """

        return self._axl.doAuthenticateUser(**kwargs)

    @cucm_logging
    def axlDoDeviceLogin(self, **kwargs: dict):

        """
        AXL Do Object Method.
        :param kwargs:      Expected Fields:
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
    def axlDoDeviceLogout(self, **kwargs: dict):

        """
        AXL Do Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"deviceName": "str"}`
        :return:
        """

        return self._axl.doDeviceLogout(**kwargs)

    @cucm_logging
    def axlDoLdapSync(self, **kwargs: dict):

        """
        AXL Do Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid.UUID", "sync": "bool"}`
                            or
                            `kwargs = {"name": "str", "sync": "bool"}`
        :return:
        """

        return self._axl.doLdapSync(**kwargs)

    @cucm_logging
    def axlGetDeviceProfile(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Get Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return serialize_object(self._axl.getDeviceProfile(**kwargs)["return"]["deviceProfile"], dict)

    @cucm_logging
    def axlGetLine(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Get Object Method.
        :param kwargs:      Expected Fields:
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
    def axlGetLineGroup(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Get Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return serialize_object(self._axl.getLineGroup(**kwargs)["return"]["lineGroup"], dict)

    @cucm_logging
    def axlGetPhone(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Get Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return serialize_object(self._axl.getPhone(**kwargs)["return"]["phone"], dict)

    @cucm_logging
    def axlGetRemoteDestination(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Get Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"destination": "str"}`
        :return:
        """

        return serialize_object(self._axl.getRemoteDestination(**kwargs)["return"]["remoteDestination"], dict)

    @cucm_logging
    def axlGetRemoteDestinationProfile(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Get Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return serialize_object(
            self._axl.getRemoteDestinationProfile(**kwargs)["return"]["remoteDestinationProfile"], dict)

    @cucm_logging
    def axlGetTranslationPattern(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Get Object Method.
        :param kwargs:      Expected Fields:
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
    def axlGetUser(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Get Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"userid": "str"}`
        :return:
        """

        return serialize_object(self._axl.getUser(**kwargs)["return"]["user"], dict)

    @cucm_logging
    def axlRemoveDeviceProfile(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Remove Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return self._axl.removeDeviceProfile(**kwargs)

    @cucm_logging
    def axlRemoveLine(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Remove Object Method.
        :param kwargs:      Expected Fields:
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
    def axlRemoveLineGroup(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Remove Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return self._axl.removeLineGroup(**kwargs)

    @cucm_logging
    def axlRemovePhone(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Remove Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return self._axl.removePhone(**kwargs)

    @cucm_logging
    def axlRemoveRemoteDestination(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Remove Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"destination": "str"}`
        :return:
        """

        return self._axl.removeRemoteDestination(**kwargs)

    @cucm_logging
    def axlRemoveRemoteDestinationProfile(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Remove Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"name": "str"}`
        :return:
        """

        return self._axl.removeRemoteDestinationProfile(**kwargs)

    @cucm_logging
    def axlRemoveTranslationPattern(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Remove Object Method.
        :param kwargs:      Expected Fields:
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
    def axlRemoveUser(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Remove Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid.UUID"}`
                            or
                            `kwargs = {"userid": "str"}`
        :return:
        """

        return self._axl.removeUser(**kwargs)

    @cucm_logging
    def axlResetPhone(self, **kwargs: dict):

        """
        AXL Reset Object Method.
        :param kwargs:      Minimum Required Parameters:
                            param = {"uuid": "uuid.UUID"}
                            or
                            param = {"name": "str"}
        :return:
        """

        return self._axl.resetPhone(**kwargs)

    @cucm_logging
    def axlRestartPhone(self, **kwargs: dict):

        """
        AXL Restart Object Method.
        :param kwargs:      Minimum Required Parameters:
                            param = {"uuid": "uuid.UUID"}
                            or
                            param = {"name": "str"}
        :return:
        """

        return self._axl.restartPhone(**kwargs)

    def sqlExecuteQuery(self, sql_query: str) -> Union[tuple[dict, ...], None]:

        """
        SQL Request to the Cisco UCM DB Informix.
        :param sql_query:   SQL Query Expression
        :return:
        """

        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlSearchCallPickupGroup(self, **kwargs) -> Union[tuple[dict, ...], None]:

        """
        SQL Search Object Method.

        * criterion: `Name`, `Description`, `Pattern`, `Member Line Number`, `Member Line Description`
        * value: Search Value String

        :param kwargs:  Expected Fields: `kwargs = {"criterion": "Enum", "value": "str"}`
        :return:
        """

        validated_data = CucmSqlSearchCallPickupGroupModel(**kwargs).model_dump()
        sql_query = """SELECT cpg.pkid AS uuid,
                              cpg.name,
                              npg.description,
                              npg.dnorpattern AS pattern,
                              rp.name AS partition,
                              npm.dnorpattern AS line,
                              rpm.name AS line_partition,
                              npm.description AS line_description
                         FROM pickupgroup cpg
                    LEFT JOIN numplan npg ON cpg.fknumplan_pickup = npg.pkid
                    LEFT JOIN routepartition rp ON npg.fkroutepartition = rp.pkid
                    LEFT JOIN pickupgrouplinemap pglm ON pglm.fkpickupgroup = cpg.pkid
                    LEFT JOIN numplan npm ON pglm.fknumplan_line = npm.pkid
                    LEFT JOIN routepartition rpm ON npm.fkroutepartition = rpm.pkid
                        WHERE LOWER({obj}) LIKE '%{val}%'
                          AND npg.tkpatternusage = '4'
                     ORDER BY cpg.name""".format(obj=validated_data["criterion"], val=validated_data["value"].lower())
        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlSearchDevice(self, **kwargs: dict) -> Union[tuple[dict, ...], None]:

        """
        SQL Search Object Method.

        * criterion:Search By: `Name`, `Description`, `Line Number`, `Line Description`, `Userid`, `Device Pool`,
          `Device Type`
        * value: Search Value String

        :param kwargs:  Expected Fields: `kwargs = {"criterion": "Enum", "value": "str"}`
        :return:
        """

        validated_data = CucmSqlSearchDeviceModel(**kwargs).model_dump()
        sql_query = """SELECT d.pkid,
                              d.name,
                              d.description,
                              dp.name AS device_pool,
                              np.dnorpattern AS line,
                              rp.name AS line_partition,
                              np.description AS line_description,
                              tc.name AS class,
                              tm.name AS model,
                              eu.pkid AS pkid_end_user,
                              eu.userid, 
                              eu.displayname AS display_name,
                              eu_rdp.pkid AS pkid_end_user_rdp,
                              eu_rdp.userid AS userid_rdp,
                              eu_rdp.displayname AS display_name_rdp
                         FROM device d
                    LEFT JOIN devicenumplanmap dnpm ON dnpm.fkdevice = d.pkid
                    LEFT JOIN numplan np ON dnpm.fknumplan = np.pkid
                    LEFT JOIN routepartition rp ON np.fkroutepartition = rp.pkid
                    LEFT JOIN devicepool dp ON d.fkdevicepool = dp.pkid
                    LEFT JOIN typemodel tm ON d.tkmodel=tm.enum
                    LEFT JOIN typeclass tc ON d.tkclass=tc.enum
                    LEFT JOIN typeproduct tprod ON tprod.tkmodel = d.tkmodel
                    LEFT JOIN enduser eu ON d.fkenduser=eu.pkid
                    LEFT JOIN enduser eu_rdp ON d.fkenduser_mobility=eu_rdp.pkid
                        WHERE LOWER({obj}) LIKE '%{val}%'
                          AND (d.tkclass = '1' OR d.tkclass = '20' OR d.tkclass = '254')
                          AND d.name NOT LIKE 'ModelProfile%'
                     ORDER BY d.name""".format(obj=validated_data["criterion"], val=validated_data["value"].lower())
        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlSearchEndUser(self, **kwargs: dict) -> Union[tuple[dict, ...], None]:

        """
        SQL Search Object Method.

        * criterion: Search By: `Userid`, `Display Name`, `Last Name`, `First Name`, `Phone Number`, `Mobile Number`,
          `Email`, `Directory URI`
        * value: Search Value String

        :param kwargs:  Expected Fields: `kwargs = {"criterion": "Enum", "value": "str"}`
        :return:
        """

        validated_data = CucmSqlSearchEndUserModel(**kwargs).model_dump()
        sql_query = """SELECT eu.pkid,
                              eu.userid,
                              eu.displayname AS display_name,
                              eu.telephonenumber AS phone_number,
                              eu.mobile AS mobile_number,
                              eu.mailid,
                              eu.department,
                              eu.title,
                              eu.fkdirectorypluginconfig AS user_type,
                              eu.status AS user_status
                         FROM enduser eu
                        WHERE LOWER({obj}) LIKE '%{val}%' 
                     ORDER BY eu.userid""".format(obj=validated_data["criterion"], val=validated_data["value"].lower())
        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlSearchLineGroup(self, **kwargs: dict) -> Union[tuple[dict, ...], None]:

        """
        SQL Search Object Method.

        * criterion: `Name`, `Member Line Number`, `Member Line Description`
        * value: Search Value String

        :param kwargs:  Expected Fields: `kwargs = {"criterion": "Enum", "value": "str"}`
        :return:
        """

        validated_data = CucmSqlSearchLineGroupModel(**kwargs).model_dump()
        sql_query = """SELECT lg.pkid,
                              lg.name,
                              tda.name AS algorithm,
                              np.dnorpattern AS line,
                              rp.name AS line_partition,
                              np.description AS line_description,
                              lgnpm.lineselectionorder AS line_index
                         FROM linegroup lg
                    LEFT JOIN linegroupnumplanmap lgnpm ON lgnpm.fklinegroup = lg.pkid
                    LEFT JOIN typedistributealgorithm tda ON lg.tkdistributealgorithm = tda.enum
                    LEFT JOIN numplan np ON lgnpm.fknumplan = np.pkid
                    LEFT JOIN routepartition rp ON np.fkroutepartition = rp.pkid
                        WHERE LOWER({obj}) LIKE '%{val}%' 
                     ORDER BY lg.name, lgnpm.lineselectionorder""".format(
            obj=validated_data["criterion"], val=validated_data["value"].lower()
        )
        return self.__cucm_sql_execute(sql_query=sql_query)

    def sqlSearchTranslationPattern(self, **kwargs: dict) -> Union[tuple[dict, ...], None]:

        """
        SQL Search Object Method.

        * criterion: `Pattern`, `Description`, `Partition`, `Calling Search Space`, `Called Party Transform Mask`,
          `Prefix Digits Out`
        * value: Search Value String

        :param kwargs:  Expected Fields: `kwargs = {"criterion": "Enum", "value": "str"}`
        :return:
        """

        validated_data = CucmSqlSearchTranslationPatternModel(**kwargs).model_dump()
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
                    LEFT JOIN routepartition rp ON np.fkroutepartition = rp.pkid
                    LEFT JOIN callingsearchspace css ON np.fkcallingsearchspace_translation = css.pkid
                    LEFT JOIN typepatternrouteclass rc ON np.tkpatternrouteclass = rc.enum
                        WHERE LOWER({obj}) LIKE '%{val}%'
                          AND np.tkpatternusage = '3'
                     ORDER BY np.dnorpattern""".format(
            obj=validated_data["criterion"], val=validated_data["value"].lower()
        )
        return self.__cucm_sql_execute(sql_query=sql_query)
