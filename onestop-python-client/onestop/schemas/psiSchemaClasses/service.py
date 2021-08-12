from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, List, Optional

from undictify import type_checked_constructor

from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.link import Link
from onestop.schemas.psiSchemaClasses.org.cedar.schemas.avro.psi.responsible_party import ResponsibleParty


@type_checked_constructor()
@dataclass
class Service:
    title: Optional[str]
    alternateTitle: Optional[str]
    description: Optional[str]
    date: Optional[str]
    dateType: Optional[str]
    pointOfContact: Optional[ResponsibleParty]
    operations: List[Link]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "name": "Service",
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
                "name": "alternateTitle",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "description",
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
                "name": "dateType",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "pointOfContact",
                "type": [
                    "null",
                    "org.cedar.schemas.avro.psi.ResponsibleParty"
                ],
                "default": null
            },
            {
                "name": "operations",
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
    ) -> 'Service':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
