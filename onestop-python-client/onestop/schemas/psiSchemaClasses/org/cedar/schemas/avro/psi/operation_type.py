from enum import Enum
from typing import ClassVar


class OperationType(Enum):
    """
    The types of metadata relationships which can be represented in the PSI system
    """
    NO_OP = "NO_OP"
    ADD = "ADD"
    REMOVE = "REMOVE"

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "enum",
        "namespace": "org.cedar.schemas.avro.psi",
        "name": "OperationType",
        "doc": "The specific operation to execute, mainly for PATCH-method input messages. Use default of NO_OP for when the method is unambiguous on its own",
        "symbols": [
            "NO_OP",
            "ADD",
            "REMOVE"
        ]
    }"""