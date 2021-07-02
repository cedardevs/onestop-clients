from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional

from undictify import type_checked_constructor
from .relationship_type import RelationshipType

@type_checked_constructor()
@dataclass
class Relationship:
    """
    Record of a relationship to another object in inventory
    """
    type: Optional[RelationshipType]

    #: The id of the related object
    id: str

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "name": "Relationship",
        "namespace": "org.cedar.schemas.avro.psi",
        "doc": "Record of a relationship to another object in inventory",
        "fields": [
            {
                "name": "type",
                "type": [
                    "null",
                    "org.cedar.schemas.avro.psi.RelationshipType"
                ],
                "default": null
            },
            {
                "name": "id",
                "type": "string",
                "doc": "The id of the related object"
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
    ) -> 'Relationship':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
