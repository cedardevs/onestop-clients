from enum import Enum
from typing import ClassVar


class MultiPolygonType(Enum):
    MultiPolygon = 'MultiPolygon'

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "MultiPolygonType",
        "type": "enum",
        "symbols": [
            "MultiPolygon"
        ]
}"""
