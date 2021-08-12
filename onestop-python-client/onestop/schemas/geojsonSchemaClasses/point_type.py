from enum import Enum
from typing import ClassVar


class PointType(Enum):
    Point = 'Point'

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "PointType",
        "type": "enum",
        "symbols": [
            "Point"
        ]
}"""
