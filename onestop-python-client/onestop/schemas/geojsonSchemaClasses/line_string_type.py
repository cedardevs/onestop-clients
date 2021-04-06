from enum import Enum
from typing import ClassVar


class LineStringType(Enum):
    LineString = 'LineString'

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "LineStringType",
        "type": "enum",
        "symbols": [
            "LineString"
        ]
}"""
