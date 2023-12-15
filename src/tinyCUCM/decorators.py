import logging
from requests.exceptions import ConnectionError, HTTPError, ProxyError, RequestException, Timeout
from zeep.exceptions import Fault, ValidationError
from .exceptions import (
    CucmAxlSessionError,
    CucmBadRequestError,
    CucmConnectionError,
    CucmUnauthorizedError,
    CucmUnexpectedError
)


""" ######################################################### """
""" ****************** TINY CUCM DECORATORS ***************** """
""" ######################################################### """


def cucm_logging(cucm_method):

    """
    Connection & Methods Logging Decorator
    :param cucm_method: CUCM Method
    :return:
    """

    def wrapped(self, *args, **kwargs):

        """
        Connection & Methods Log Wrapper
        :return:
        """

        log_message = f"@ CUCM {repr(cucm_method.__name__)} Method @ - {{message}}"
        logging.debug(log_message.format(message=f"Query Params:\nArgs: {args}\nKwargs: {kwargs}."))

        try:
            # Return Union[tuple, dict, None]
            return cucm_method(self, *args, **kwargs)

        except (AttributeError, TypeError) as err:
            err = str(err)
            if "NoneType" in err:
                logging.error(log_message.format(message=f"Error Detail:\n{err}."))
                raise CucmAxlSessionError("Session FailedDependency error occurred. AXL is None.")
            elif ("Service has no operation" in err
                  or "got an unexpected keyword argument" in err
                  or "object has no attribute" in err):
                # "Service has no operation 'method name'" - Method Error
                # "got an unexpected keyword argument" - Invalid Argument for AXL Methods (Example: "uud" vs. "uuid")
                logging.error(log_message.format(message=f"Error Detail:\n{err}."))
                raise CucmBadRequestError("BadRequest error occurred.")

            logging.error(log_message.format(message=f"Error Detail:\n{err}."))
            raise CucmUnexpectedError("Unexpected error occurred.")

        except (Fault, ValidationError) as err:
            history = self._cucm_history_show()
            if "HTTP Status 401" in history:
                raise CucmUnauthorizedError("Unauthorized error occurred.")
            elif "<axlcode>5003</axlcode>" in history or "<axlcode>5007</axlcode>" in history:
                # Only for AXL Requests - 404 Not Found
                # Do or Get Request - AXLCode: <axlcode>5007</axlcode>
                # ("Item not valid: The specified {{CUCM Object}} was not found")
                # UpdateRequest - AXLCode: <axlcode>5003</axlcode> ("{{CUCM Object}} not found")
                logging.warning(log_message.format(message=f"Error Detail:\n{err}."))
                return None
            else:
                # For Invalid SQL Queries. AXLCode: 201 ("A syntax error has occurred")
                logging.error(log_message.format(message=f"Error Detail:\n{err}."))
                logging.error(log_message.format(message=f"History:\n{history}."))
                raise CucmBadRequestError("BadRequest error occurred.")

        except (ConnectionError, HTTPError, ProxyError, RequestException, Timeout) as err:
            logging.error(log_message.format(message=f"Error Detail:\n{err}"))
            raise CucmConnectionError("Connection has been failed.")

        except Exception as err:
            logging.error(log_message.format(message=f"Error Detail: {repr(err)}."))
            logging.error(log_message.format(message=f"History:\n{self._cucm_history_show()}"))
            raise CucmUnexpectedError("Unexpected error occurred.")

    return wrapped
