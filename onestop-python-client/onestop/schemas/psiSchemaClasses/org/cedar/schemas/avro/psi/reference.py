from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, List, Optional

from undictify import type_checked_constructor

from .link import Link


@type_checked_constructor()
@dataclass
class Reference:
    title: Optional[str]
    date: Optional[str]
    links: List[Link]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "Reference",
        "namespace": "org.cedar.schemas.avro.psi",
        "type": "record",
        "fields": [
            {
                "name": "title",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "date",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "links",
                "type": {
                    "type": "array",
                    "items": "org.cedar.schemas.avro.psi.Link"
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
    ) -> 'Reference':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
