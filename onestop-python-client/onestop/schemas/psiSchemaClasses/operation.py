from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional

from undictify import type_checked_constructor


@type_checked_constructor()
@dataclass
class Operation:
    operationDescription: Optional[str]
    operationIdentifier: Optional[str]
    operationStatus: Optional[str]
    operationType: Optional[str]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "Operation",
        "type": "record",
        "fields": [
            {
                "name": "operationDescription",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "operationIdentifier",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "operationStatus",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "operationType",
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
    ) -> 'Operation':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
