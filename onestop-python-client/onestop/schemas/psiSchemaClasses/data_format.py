from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional

from undictify import type_checked_constructor


@type_checked_constructor()
@dataclass
class DataFormat:
    name: Optional[str]
    version: Optional[str]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "DataFormat",
        "type": "record",
        "fields": [
            {
                "name": "name",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "version",
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
    ) -> 'DataFormat':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
