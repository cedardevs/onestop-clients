from enum import Enum
from typing import ClassVar


class TimeRangeDescriptor(Enum):
    AMBIGUOUS = 'AMBIGUOUS'
    BACKWARDS = 'BACKWARDS'
    BOUNDED = 'BOUNDED'
    INSTANT = 'INSTANT'
    INVALID = 'INVALID'
    ONGOING = 'ONGOING'
    NOT_APPLICABLE = 'NOT_APPLICABLE'
    UNDEFINED = 'UNDEFINED'

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "enum",
        "name": "TimeRangeDescriptor",
        "symbols": [
            "AMBIGUOUS",
            "BACKWARDS",
            "BOUNDED",
            "INSTANT",
            "INVALID",
            "ONGOING",
            "NOT_APPLICABLE",
            "UNDEFINED"
        ]
    }"""
