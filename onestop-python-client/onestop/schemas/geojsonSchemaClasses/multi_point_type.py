from enum import Enum
from typing import ClassVar


class MultiPointType(Enum):
    MultiPoint = 'MultiPoint'

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "MultiPointType",
        "type": "enum",
        "symbols": [
            "MultiPoint"
        ]
}"""
