"""
DANK MEMER IMGEN API CLIENT
---------------------------
Copyright: Copyright 2019 Melms Media LLC
License: MIT

"""


class NoTokenError(Exception):
    """Exception that is raised when an instance of img-client is instanced without a token"""
    pass


class IncorrectTokenError(Exception):
    """Exception that is raised when an instance of img-client is instanced without a token"""
    pass


class Forbidden(Exception):
    """Exception that is raised when you can't access an endpoint"""
    pass


class BadRequest(Exception):
    """Exception that is raised when invalid data is sent to the server"""
    def __init__(self, m):
        pass


class HTTPError(Exception):
    """Generic exception for server errors"""
    def __init__(self, m):
        pass


class NotFound(Exception):
    """Exception that is called when the endpoint could not be found"""
    def __init__(self, m):
        pass


class NoEndpointsError(Exception):
    """Exception that is raised when the list of endpoints could not be fetched"""
    pass


class MissingParameterError(Exception):
    """Exception that is raised when an endpoint requires an parameter, but it is not passed"""
    def __init__(self, m):
        pass


class NoDiscordInstalled(Exception):
    """Exception that is raised when get_as_discord is called without the discord.py library installed"""
    pass
