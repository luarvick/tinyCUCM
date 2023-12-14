import logging


""" ######################################################### """
""" ****************** TINY CUCM EXCEPTIONS ***************** """
""" ######################################################### """


class CucmBaseError(Exception):

    """
        tinyCUCM. Base Error.
        """

    def __init__(self, message: str = None):
        self.message = message
        if self.message:
            logging.error(self.message)

    def __str__(self):
        return self.message


class CucmAxlSessionError(CucmBaseError):
    pass


class CucmBadRequestError(CucmBaseError):
    pass


class CucmConnectionError(CucmBaseError):
    pass


class CucmSessionError(CucmBaseError):
    pass


class CucmUnauthorizedError(CucmBaseError):
    pass


class CucmUnexpectedError(CucmBaseError):
    pass
