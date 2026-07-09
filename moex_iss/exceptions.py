class ISSException(Exception):
    """
    Base ISS exception
    """
    pass



class ISSConnectionError(ISSException):
    pass



class ISSAuthenticationError(ISSException):
    pass



class ISSResponseError(ISSException):
    pass



class ISSPaginationError(ISSException):
    pass