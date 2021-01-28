from enum import Enum
from typing import ClassVar


class ChecksumAlgorithm(Enum):
    MD5 = 'MD5'
    SHA1 = 'SHA1'
    SHA256 = 'SHA256'
    SHA512 = 'SHA512'

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "ChecksumAlgorithm",
        "namespace": "org.cedar.schemas.avro.psi",
        "type": "enum",
        "symbols": [
            "MD5",
            "SHA1",
            "SHA256",
            "SHA512"
        ]
    }"""
