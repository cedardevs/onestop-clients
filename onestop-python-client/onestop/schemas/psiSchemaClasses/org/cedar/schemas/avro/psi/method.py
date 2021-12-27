from enum import Enum
from typing import ClassVar


class Method(Enum):
    """
    The types of metadata relationships which can be represented in the PSI system
    """
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    TRACE = 'TRACE'
    CONNECT = 'CONNECT'

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "enum",
        "namespace": "org.cedar.schemas.avro.psi",
        "name": "Method",
        "doc": "An HTTP request method",
        "symbols": [
            "HEAD",
            "OPTIONS",
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "TRACE",
            "CONNECT"
        ]
    }"""
