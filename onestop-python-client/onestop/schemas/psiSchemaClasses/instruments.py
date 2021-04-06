from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional

from undictify import type_checked_constructor


@type_checked_constructor()
@dataclass
class Instruments:
    instrumentIdentifier: Optional[str]
    instrumentType: Optional[str]
    instrumentDescription: Optional[str]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "Instruments",
        "type": "record",
        "fields": [
            {
                "name": "instrumentIdentifier",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "instrumentType",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "instrumentDescription",
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
    ) -> 'Instruments':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
