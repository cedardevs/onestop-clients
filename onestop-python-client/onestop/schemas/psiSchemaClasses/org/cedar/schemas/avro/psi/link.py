from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional

from undictify import type_checked_constructor


@type_checked_constructor()
@dataclass
class Link:
    linkName: Optional[str]
    linkProtocol: Optional[str]
    linkUrl: Optional[str]
    linkDescription: Optional[str]
    linkFunction: Optional[str]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "Link",
        "namespace": "org.cedar.schemas.avro.psi",
        "type": "record",
        "fields": [
            {
                "name": "linkName",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "linkProtocol",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "linkUrl",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "linkDescription",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "linkFunction",
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
    ) -> 'Link':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
