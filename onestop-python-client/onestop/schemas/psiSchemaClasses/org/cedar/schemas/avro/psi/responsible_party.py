from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional

from undictify import type_checked_constructor


@type_checked_constructor()
@dataclass
class ResponsibleParty:
    individualName: Optional[str]
    organizationName: Optional[str]
    positionName: Optional[str]
    role: Optional[str]
    email: Optional[str]
    phone: Optional[str]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "ResponsibleParty",
        "namespace": "org.cedar.schemas.avro.psi",
        "type": "record",
        "fields": [
            {
                "name": "individualName",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "organizationName",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "positionName",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "role",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "email",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "phone",
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
    ) -> 'ResponsibleParty':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
