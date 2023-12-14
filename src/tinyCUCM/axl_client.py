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
        All Methods Collection.
        :return:
        """

        return tuple(sorted([str(method[0]) for method in self._axl]))

    def sqlExecuteQuery(self, sql_query: str) -> Union[tuple[dict, ...], None]:

        """
        SQL Request to the Cisco UCM DB Informix.
        :param sql_query:   SQL Query Expression
        :return:
        """

        return self.__cucm_sql_execute(sql_query=sql_query)
