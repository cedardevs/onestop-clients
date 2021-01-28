from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional

from undictify import type_checked_constructor


@type_checked_constructor()
@dataclass
class Publishing:
    """
    Record describing whether the object this is in reference to should be publicly available, and if not, for how long it should remain private
    """

    #: Indicates if the object is private or not
    isPrivate: bool

    #: The time, stored as the number of milliseconds from the unix epoch, until which the isPrivate value is valid and after which it is reversed
    until: Optional[int]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "namespace": "org.cedar.schemas.avro.psi",
        "name": "Publishing",
        "doc": "Record describing whether the object this is in reference to should be publicly available, and if not, for how long it should remain private",
        "fields": [
            {
                "name": "isPrivate",
                "type": "boolean",
                "doc": "Indicates if the object is private or not",
                "default": false
            },
            {
                "name": "until",
                "type": [
                    "null",
                    "long"
                ],
                "doc": "The time, stored as the number of milliseconds from the unix epoch, until which the isPrivate value is valid and after which it is reversed",
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
    ) -> 'Publishing':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
