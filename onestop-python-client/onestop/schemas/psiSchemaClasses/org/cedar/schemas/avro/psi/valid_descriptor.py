from enum import Enum
from typing import ClassVar


class ValidDescriptor(Enum):
    VALID = 'VALID'
    INVALID = 'INVALID'
    UNDEFINED = 'UNDEFINED'

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "ValidDescriptor",
        "namespace": "org.cedar.schemas.avro.psi",
        "type": "enum",
        "doc": "The types of metadata records which can be represented in the PSI system",
        "symbols": [
            "VALID",
            "INVALID",
            "UNDEFINED"
        ]
    }"""