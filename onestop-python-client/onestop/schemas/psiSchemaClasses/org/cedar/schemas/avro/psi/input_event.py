from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional

from undictify import type_checked_constructor

from .method import Method
from .operation_type import OperationType


@type_checked_constructor()
@dataclass
class InputEvent:
    """
    Record describing when and what happened when an input was received
    """

    #: The timestamp of when the event occurred, stored as the number of milliseconds from the unix epoch
    timestamp: Optional[int]

    #: The HTTP method associated with this event
    method: Optional[Method]

    #: The source associated with this event
    source: Optional[str]

    #: The specific operation to execute, mainly for PATCH-method input messages. Use NO_OP for when the method is unambiguous on its own.
    operation: Optional[OperationType]

    #: Whether or not this event caused errors to occur when creating the AggregatedInput.
    failedState: bool

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "namespace": "org.cedar.schemas.avro.psi",
        "name": "InputEvent",
        "doc": "Record describing when and what happened when an input was received",
        "fields": [
            {
                "name": "timestamp",
                "type": [
                    "null",
                    "long"
                ],
                "doc": "The timestamp of when the event occurred, stored as the number of milliseconds from the unix epoch",
                "default": null
            },
            {
                "name": "method",
                "type": [
                    "null",
                    "org.cedar.schemas.avro.psi.Method"
                ],
                "doc": "The HTTP method associated with this event",
                "default": null
            },
            {
                "name": "source",
                "type": [
                    "null",
                    "string"
                ],
                "doc": "The source associated with this event",
                "default": null
            },
            {
                "name": "operation",
                "type": [
                    "null",
                    "org.cedar.schemas.avro.psi.OperationType"
                ],
                "doc": "The specific operation to execute, mainly for PATCH-method input messages. Use NO_OP for when the method is unambiguous on its own.",
                "default": null
            },
            {
                "name": "failedState",
                "type": "boolean",
                "doc": "Whether or not this event caused errors to occur when creating the AggregatedInput.",
                "default": false
            }
        ]
    }"""

    def to_dict(self) -> Dict:
        """
        Returns a dictionary version of this instance.
        """
        return asdict(self)

    @classmethod
    def from_dict(
            cls,
            the_dict: Dict
    ) -> 'InputEvent':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
