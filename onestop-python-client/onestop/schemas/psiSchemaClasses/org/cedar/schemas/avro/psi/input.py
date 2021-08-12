from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional

from undictify import type_checked_constructor

from .method import Method
from .operation_type import OperationType
from .record_type import RecordType


@type_checked_constructor()
@dataclass
class Input:
    """
    The raw input for a metadata record, plus information about how the input was sent
    """

    #: The type of record represented by this input
    type: Optional[RecordType]

    #: The raw input content as a string
    content: Optional[str]

    #: The MIME type associated with the value of the content field
    contentType: Optional[str]

    #: The HTTP method used to send the input or which describes the verb associated with the input in general
    method: Optional[Method]

    #: The source of the input, e.g. the name of an external system which produced this input record
    source: Optional[str]

    #: The specific operation to execute, mainly for PATCH-method input messages. Use NO_OP for when the method is unambiguous on its own.
    operation: Optional[OperationType]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "namespace": "org.cedar.schemas.avro.psi",
        "name": "Input",
        "doc": "The raw input for a metadata record, plus information about how the input was sent",
        "fields": [
            {
                "name": "type",
                "type": [
                    "null",
                    "org.cedar.schemas.avro.psi.RecordType"
                ],
                "doc": "The type of record represented by this input",
                "default": null
            },
            {
                "name": "content",
                "type": [
                    "null",
                    "string"
                ],
                "doc": "The raw input content as a string",
                "default": null
            },
            {
                "name": "contentType",
                "type": [
                    "null",
                    "string"
                ],
                "doc": "The MIME type associated with the value of the content field",
                "default": null
            },
            {
                "name": "method",
                "type": [
                    "null",
                    "org.cedar.schemas.avro.psi.Method"
                ],
                "doc": "The HTTP method used to send the input or which describes the verb associated with the input in general",
                "default": null
            },
            {
                "name": "source",
                "type": [
                    "null",
                    "string"
                ],
                "doc": "The source of the input, e.g. the name of an external system which produced this input record",
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
    ) -> 'Input':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
