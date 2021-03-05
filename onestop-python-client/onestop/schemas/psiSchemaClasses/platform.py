from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, List, Optional

from undictify import type_checked_constructor


@type_checked_constructor()
@dataclass
class Platform:
    platformIdentifier: Optional[str]
    platformDescription: Optional[str]
    platformSponsor: List[str]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "Platform",
        "type": "record",
        "fields": [
            {
                "name": "platformIdentifier",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "platformDescription",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "platformSponsor",
                "type": {
                    "type": "array",
                    "items": "string"
                },
                "default": []
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
    ) -> 'Platform':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
