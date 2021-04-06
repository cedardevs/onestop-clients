from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional

from undictify import type_checked_constructor


@type_checked_constructor()
@dataclass
class TemporalBounding:

    beginDate: Optional[str]
    beginIndeterminate: Optional[str]
    endDate: Optional[str]
    endIndeterminate: Optional[str]
    instant: Optional[str]
    instantIndeterminate: Optional[str]
    description: Optional[str]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "name": "TemporalBounding",
        "namespace": "org.cedar.schemas.avro.psi",
        "fields": [
            {
                "name": "beginDate",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "beginIndeterminate",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "endDate",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "endIndeterminate",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "instant",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "instantIndeterminate",
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
    ) -> 'TemporalBounding':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
