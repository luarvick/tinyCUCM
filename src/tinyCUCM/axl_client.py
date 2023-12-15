from typing import Iterable, Union
from zeep.helpers import serialize_object
from .decorators import cucm_logging
from .settings import CucmSettings


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
    def __cucm_sql_execute(self, sql_query: str) -> Union[tuple, None]:

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
    def axlGetDeviceProfile(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Get Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid"}`
                            or
                            `kwargs = {"name": "name"}`
        :return:
        """

        return serialize_object(self._axl.getDeviceProfile(**kwargs)["return"]["deviceProfile"], dict)

    @cucm_logging
    def axlGetLine(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Get Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid"}`
                            or
                            `kwargs = {"pattern": "pattern"}`
                            or
                            `kwargs = {
                                "pattern": "pattern",
                                "routePartitionName": "routePartitionName"
                            }`
        :return:
        """

        return serialize_object(self._axl.getLine(**kwargs)["return"]["line"], dict)

    @cucm_logging
    def axlGetPhone(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Get Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid"}`
                            or
                            `kwargs = {"name": "name"}`
        :return:
        """

        return serialize_object(self._axl.getPhone(**kwargs)["return"]["phone"], dict)

    @cucm_logging
    def axlGetRemoteDestination(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Get Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid"}`
                            or
                            `kwargs = {"destination": "destination"}`
        :return:
        """

        return serialize_object(self._axl.getRemoteDestination(**kwargs)["return"]["remoteDestination"], dict)

    @cucm_logging
    def axlGetRemoteDestinationProfile(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Get Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid"}`
                            or
                            `kwargs = {"name": "name"}`
        :return:
        """

        return serialize_object(
            self._axl.getRemoteDestinationProfile(**kwargs)["return"]["remoteDestinationProfile"], dict)

    @cucm_logging
    def axlGetTranslationPattern(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Get Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid"}`
                            or
                            `kwargs = {"pattern": "pattern"}`
                            or
                            `kwargs = {
                                "pattern": "pattern",
                                "routePartitionName": "routePartitionName"
                            }`
        :return:
        """

        return serialize_object(self._axl.getTransPattern(**kwargs)["return"]["transPattern"], dict)

    @cucm_logging
    def axlRemoveDeviceProfile(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Remove Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid"}`
                            or
                            `kwargs = {"name": "name"}`
        :return:
        """

        return self._axl.removeDeviceProfile(**kwargs)

    @cucm_logging
    def axlRemoveLine(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Remove Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid"}`
                            or
                            `kwargs = {"pattern": "pattern"}`
                            or
                            `kwargs = {
                                "pattern": "pattern",
                                "routePartitionName": "routePartitionName"
                            }`
        :return:
        """

        return self._axl.removeLine(**kwargs)

    @cucm_logging
    def axlRemovePhone(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Remove Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid"}`
                            or
                            `kwargs = {"name": "name"}`
        :return:
        """

        return self._axl.removePhone(**kwargs)

    @cucm_logging
    def axlRemoveRemoteDestination(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Remove Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid"}`
                            or
                            `kwargs = {"destination": "destination"}`
        :return:
        """

        return self._axl.removeRemoteDestination(**kwargs)

    @cucm_logging
    def axlRemoveRemoteDestinationProfile(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Remove Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid"}`
                            or
                            `kwargs = {"name": "name"}`
        :return:
        """

        return self._axl.removeRemoteDestinationProfile(**kwargs)

    @cucm_logging
    def axlRemoveTranslationPattern(self, **kwargs: dict) -> Union[dict, None]:

        """
        AXL Remove Object Method.
        :param kwargs:      Expected Fields:
                            `kwargs = {"uuid": "uuid"}`
                            or
                            `kwargs = {"pattern": "pattern"}`
                            or
                            `kwargs = {
                                "pattern": "pattern",
                                "routePartitionName": "routePartitionName"
                            }`
        :return:
        """

        return self._axl.removeTransPattern(**kwargs)

    def sqlExecuteQuery(self, sql_query: str) -> Union[tuple[dict, ...], None]:

        """
        SQL Request to the Cisco UCM DB Informix.
        :param sql_query:   SQL Query Expression
        :return:
        """

        return self.__cucm_sql_execute(sql_query=sql_query)
