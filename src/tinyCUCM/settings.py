import logging, os
from lxml import etree
from requests import Session
from requests.auth import HTTPBasicAuth
from typing import Union
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from zeep import Client
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.proxy import ServiceProxy
from zeep.transports import Transport

from .exceptions import CucmSessionError


""" ######################################################### """
""" ******************* TINY CUCM SETTINGS ****************** """
""" ######################################################### """


class CucmSettings:

    """
        tinyCUCM Settings. Cisco Unified Call Manager Configuration & Sessions Class.
        """

    def __init__(self, **kwargs):
        super(CucmSettings, self).__init__()

        disable_warnings(InsecureRequestWarning)

        self._axl = None
        self._axl_client = None     # Workaround for CSCvq98025 (axlAddRemoteDestination)
        self._axl_transport = None  # Workaround for CSCvq98025 (axlAddRemoteDestination)
        self._ccs = None            # Control Center Services
        self._ris = None            # Real-time Information Server
        self._ris_factory = None    # Real-time Information Server

        self.__pub_fqdn: str = kwargs.get("pub_fqdn")
        self.__pub_version: str = kwargs.get("pub_version")
        self.__user_login: str = kwargs.get("user_login")
        self.__user_password: str = kwargs.get("user_password")
        self.__toolkit_path: str = kwargs.get("toolkit_path")
        self.__cert_path: str = kwargs.get("cert_path")
        self.__session_verify: bool = kwargs.get("session_verify")
        self.__session_timeout: int = kwargs.get("session_timeout") or 20

        self.__ccs_wsdl_filename: str = kwargs.get("ccs_wsdl_filename") or "wsdlControlCenterServices.xml"
        self.__ris_wsdl_filename: str = kwargs.get("ris_wsdl_filename") or "wsdlRISService70.xml"

        self.__cucm_history = HistoryPlugin()

        self.__cucm_axl_service()
        self.__cucm_ccs_service()
        self.__cucm_ris_service()

    @property
    def _cucm_publisher_property(self) -> str:

        """
        CUCM Publisher Property.
        :return:
        """

        return self.__pub_fqdn

    def _cucm_history_show(self) -> str:

        """
        History Show.
        :return:
        """

        history_error = "Unexpected history error occurred"
        try:
            for item in [self.__cucm_history.last_sent, self.__cucm_history.last_received]:
                try:
                    string = etree.tostring(item["envelope"], encoding="unicode", pretty_print=True)
                except TypeError:
                    return history_error
            return string
        except IndexError:
            return history_error

    def __cucm_session_create(self) -> Session:

        """
        Session Create.
        :return:
        """

        session = Session()
        session.verify = False
        if self.__session_verify:
            # TODO: Cert Check
            session.verify = self.__cert_path
            if not os.path.isfile(self.__cert_path):
                raise FileNotFoundError(f"{repr(self.__cert_path)}, certificate file not found.")
        session.auth = HTTPBasicAuth(self.__user_login, self.__user_password)
        return session

    def __cucm_axl_service(self):

        """
        AXL Service.
        :return:
        """

        log_message = "@ CUCM AXL Service @ - {message}"

        # If you're not disabling SSL verification, host should be the FQDN of the server rather than IP
        location = f"https://{self.__pub_fqdn}:8443/axl/"
        binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"
        wsdl_path = f"{self.__toolkit_path}/schema/{self.__pub_version}/AXLAPI.wsdl"
        if not os.path.isfile(wsdl_path):
            raise FileNotFoundError(f"{repr(wsdl_path)}, wsdl file not found.")

        session = self.__cucm_session_create()
        try:
            # 'Exception Value: [WinError 5] Access is denied: '.\\zeep'' fixes:
            # cache=False or cache=SqliteCache(".../axlsqltoolkit/cache_axl.db")
            self._axl_transport = Transport(
                cache=SqliteCache(f"{self.__toolkit_path}/cache_axl.db"),
                session=session,
                timeout=self.__session_timeout
            )
            self._axl_client = Client(wsdl=wsdl_path, transport=self._axl_transport, plugins=[self.__cucm_history])
            self._axl = self._axl_client.create_service(binding, location)
        except Exception as err:
            logging.error(log_message.format(message=f"Error Detail:\n{err}."))
            raise CucmSessionError("Session error occurred.")

    def __cucm_ccs_service(self, node_fqdn: str = None) -> Union[ServiceProxy, None]:

        """
        CCS (Control Center Services) Service.
        :param node_fqdn:   Cluster Node FQDN or IP Address
        :return:
        """

        log_message = "@ CUCM CCS Service @ - {message}"

        location = f"https://{self.__pub_fqdn}:8443/controlcenterservice2/services/ControlCenterServices"
        binding = "{http://schemas.cisco.com/ast/soap}ControlCenterServicesBinding"

        wsdl_path = f"{self.__toolkit_path}/{self.__ccs_wsdl_filename}"
        if not os.path.isfile(wsdl_path):
            raise FileNotFoundError(f"{repr(wsdl_path)}, wsdl file not found.")

        session = self.__cucm_session_create()
        try:
            transport = Transport(
                cache=False,
                session=session,
                timeout=self.__session_timeout
            )
            client = Client(wsdl=wsdl_path, transport=transport, plugins=[self.__cucm_history])
            if node_fqdn:
                location = f"https://{node_fqdn}:8443/controlcenterservice2/services/ControlCenterServices"
                return client.create_service(binding, location)
            self._ccs = client.create_service(binding, location)
        except Exception as err:
            logging.error(log_message.format(message=f"Error Detail:\n{err}."))
            raise CucmSessionError("Session error occurred.")

    def __cucm_ris_service(self):

        """
        RIS (Real-time Information Server) Service.
        :return:
        """

        log_message = "@ CUCM RIS Service @ - {message}"

        wsdl_path = f"{self.__toolkit_path}/{self.__ris_wsdl_filename}"
        if not os.path.isfile(wsdl_path):
            logging.warning(log_message.format(message=f"{repr(wsdl_path)}, wsdl file not found."))
            wsdl_path = f"https://{self.__pub_fqdn}:8443/realtimeservice2/services/RISService70?wsdl"
            # raise FileNotFoundError(f"{repr(wsdl_path)}, wsdl file not found.")

        session = self.__cucm_session_create()
        try:
            transport = Transport(
                cache=SqliteCache(f"{self.__toolkit_path}/cache_ris.db"),
                session=session,
                timeout=self.__session_timeout
            )
            self._ris = Client(wsdl=wsdl_path, transport=transport, plugins=[self.__cucm_history])
            self._ris_factory = self._ris.type_factory("ns0")
        except Exception as err:
            logging.error(log_message.format(message=f"Error Detail:\n{err}."))
            raise CucmSessionError("Session error occurred.")

    def _cucm_ccs_custom_node_service(self, node_fqdn: Union[str, None]) -> ServiceProxy:

        """
        CCS (Control Center Services) Service for Another Cluster Node.
        :param node_fqdn:   Cluster Node FQDN or IP Address
        :return:
        """

        return self.__cucm_ccs_service(node_fqdn=node_fqdn) if node_fqdn and node_fqdn != self.__pub_fqdn else self._ccs
