from enum import Enum
from typing import ClassVar


class MultiLineStringType(Enum):
    MultiLineString = 'MultiLineString'

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "MultiLineStringType",
        "type": "enum",
        "symbols": [
            "MultiLineString"
        ]
}"""
