class GenericException(Exception):
    __message__="Generic Exception"

    def __init__(self, message=None):
        if message is None and self.__message__ is not None:
            message = self.__message__
        self.message = message
        super().__init__(self.__message__)

class ApplicationException(GenericException):
    __message__="Application Exception"

class NotImplementedException(ApplicationException):
    __message__="Not Implemented"