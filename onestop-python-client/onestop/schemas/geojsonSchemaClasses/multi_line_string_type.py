from enum import Enum
from typing import ClassVar


class MultiLineStringType(Enum):
    MULTILINESTRING = 'MultiLineString'

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "MultiLineStringType",
        "type": "enum",
        "symbols": [
            "MultiLineString"
        ]
}"""
