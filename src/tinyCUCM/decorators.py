from requests.exceptions import ConnectionError, HTTPError, ProxyError, RequestException, Timeout
from typing import Optional
from zeep.exceptions import Fault, ValidationError

from .exceptions import (
    CucmAxlSessionError,
    CucmBadRequestError,
    CucmConnectionError,
    CucmObjNotFoundError,
    CucmUnauthorizedError,
    CucmUnexpectedError
)
from .logger import logger


""" ######################################################### """
""" ****************** TINY CUCM DECORATORS ***************** """
""" ######################################################### """


def cucm_logging(cucm_method):

    """
    Connection & Methods Logging Decorator
    :param cucm_method: CUCM Method
    :return:
    """

    def wrapper(self, *args, **kwargs):

        message = f"@ CUCM {repr(cucm_method.__name__)} Method @ - {{msg}}"
        logger.debug(message.format(msg=f"Query Params:\nArgs: {args}\nKwargs: {kwargs}."))

        try:
            # Return Union[tuple, dict, None]
            return cucm_method(self, *args, **kwargs)

        except (AttributeError, TypeError) as err:
            err = str(err)
            if "NoneType" in err:
                logger.error(message.format(msg=f"Error Detail: {repr(err)}."))
                raise CucmAxlSessionError("Session FailedDependency error occurred. Client is None.")
            elif ("Service has no operation" in err
                  or "is not in allowed get methods" in err
                  or "got an unexpected keyword argument" in err
                  or "object has no attribute" in err):
                # "Service has no operation 'method name'" - Method Error
                # "is not in allowed get methods" - Method Error (Example: wrong get axl method "getPhon")
                # "got an unexpected keyword argument" - Invalid Argument for AXL Methods (Example: "uud" vs. "uuid")
                logger.error(message.format(msg=f"Error Detail: {repr(err)}."))
                raise CucmBadRequestError(f"BadRequest error occurred. {repr(err)}")

            logger.error(message.format(msg=f"Error Detail: {repr(err)}."))
            raise CucmUnexpectedError(f"Unexpected error occurred. {repr(err)}")

        except (Fault, ValidationError) as err:
            history = self._cucm_history_show()
            if "HTTP Status 401" in history:
                raise CucmUnauthorizedError("Unauthorized error occurred.")
            elif "<axlcode>5003</axlcode>" in history or "<axlcode>5007</axlcode>" in history:
                # Only for AXL Requests - 404 Not Found
                # Do or Get Request - AXLCode: 5007 - "Item not valid: The specified {{CUCM Object}} was not found"
                # UpdateRequest - AXLCode: 5003 - "{{CUCM Object}} not found"
                logger.error(message.format(msg=f"Error Detail: {repr(err)}."))
                logger.error(message.format(msg=f"History: {history}."))
                raise CucmObjNotFoundError(f"NotFound error occurred. {repr(err)}")
            else:
                # For Invalid SQL Queries.
                # AXLCode: 201 - "A syntax error has occurred"
                # AXLCode: 217 - "Column ({{column_names}}) not found..."
                logger.error(message.format(msg=f"Error Detail: {repr(err)}."))
                logger.error(message.format(msg=f"History: {history}."))
                raise CucmBadRequestError(f"BadRequest error occurred. {repr(err)}")

        except (ConnectionError, HTTPError, ProxyError, RequestException, Timeout) as err:
            logger.error(message.format(msg=f"Error Detail: {repr(err)}"))
            raise CucmConnectionError(f"Connection has been failed. {repr(err)}")

        except Exception as err:
            logger.error(message.format(msg=f"Error Detail: {repr(err)}."))
            logger.error(message.format(msg=f"History: {self._cucm_history_show()}"))
            raise CucmUnexpectedError(f"Unexpected error occurred. {repr(err)}")

    return wrapper
