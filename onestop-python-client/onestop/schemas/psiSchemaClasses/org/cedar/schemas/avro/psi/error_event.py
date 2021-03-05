from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional

from undictify import type_checked_constructor


@type_checked_constructor()
@dataclass
class ErrorEvent:
    """
    Contains information about errors encountered while performing an operation
    """

    #: A short, human-readable summary of the problem that should not change from occurrence to occurrence of the problem.
    title: Optional[str]

    #: A human-readable explanation specific to this occurrence of the problem.
    detail: Optional[str]

    #: The HTTP status code applicable to this problem.
    status: Optional[int]

    #: An application-specific error code.
    code: Optional[int]

    #: The origination source, i.e., the application, of the error
    source: Optional[str]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "name": "ErrorEvent",
        "namespace": "org.cedar.schemas.avro.psi",
        "doc": "Contains information about errors encountered while performing an operation",
        "fields": [
            {
                "name": "title",
                "doc": "A short, human-readable summary of the problem that should not change from occurrence to occurrence of the problem.",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "detail",
                "doc": "A human-readable explanation specific to this occurrence of the problem.",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "status",
                "doc": "The HTTP status code applicable to this problem.",
                "type": [
                    "null",
                    "int"
                ],
                "default": null
            },
            {
                "name": "code",
                "doc": "An application-specific error code.",
                "type": [
                    "null",
                    "int"
                ],
                "default": null
            },
            {
                "name": "source",
                "doc": "The origination source, i.e., the application, of the error",
                "type": [
                    "null",
                    "string"
                ],
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
    ) -> 'ErrorEvent':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
