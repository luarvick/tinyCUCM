import logging, os
from lxml import etree
from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from zeep import Client
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.transports import Transport
from .exceptions import CucmSessionError


""" ######################################################### """
""" ******************* TINY CUCM SETTINGS ****************** """
""" ######################################################### """


class CucmSettings:

    """
        tinyCUCM Settings. Cisco Unified Call Manager Configuration & Sessions Class
        """

    def __init__(self, **kwargs):
        super(CucmSettings, self).__init__()

        disable_warnings(InsecureRequestWarning)

        self._axl = None
        self._ris = None
        self._ris_factory = None

        self.__pub_fqdn: str = kwargs.get("pub_fqdn")
        self.__pub_version: str = kwargs.get("pub_version")
        self.__user_login: str = kwargs.get("user_login")
        self.__user_password: str = kwargs.get("user_password")
        self.__toolkit_path: str = kwargs.get("toolkit_path")
        self.__cert_path: str = kwargs.get("cert_path")
        self.__session_verify: bool = kwargs.get("session_verify")
        self.__session_timeout: int = kwargs.get("session_timeout") or 20

        self.__ris_wsdl_filename: str = kwargs.get("ris_wsdl_filename")

        self.__cucm_history = HistoryPlugin()

        self.__cucm_axl_client()
        self.__cucm_ris_client()

    def _cucm_history_show(self) -> str:

        """
        History Show
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

    def __cucm_axl_client(self):

        """
        AXL Client.
        :return:
        """

        log_message = "@ CUCM AXL Client @ - {message}"

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
            transport = Transport(
                cache=SqliteCache(f"{self.__toolkit_path}/cache_axl.db"),
                session=session,
                timeout=self.__session_timeout
            )
            client = Client(wsdl=wsdl_path, transport=transport, plugins=[self.__cucm_history])
            self._axl = client.create_service(binding, location)
        except Exception as err:
            logging.error(log_message.format(message=f"Error Detail:\n{err}."))
            raise CucmSessionError("Session error occurred.")

    def __cucm_ris_client(self):

        """
        RIS (Real-time Information Server) Client.
        :return:
        """

        log_message = "@ CUCM RIS Client @ - {message}"

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
