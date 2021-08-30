from enum import Enum
from typing import ClassVar


class PolygonType(Enum):
    POLYGON = 'Polygon'
    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "PolygonType",
        "type": "enum",
        "symbols": [
            "Polygon"
        ]
    }"""
