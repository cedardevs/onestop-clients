from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional

from undictify import type_checked_constructor


@type_checked_constructor()
@dataclass
class SpatialBoundingAnalysis:
    #: Indicates if the analyzed record has a spatial bounding
    spatialBoundingExists: Optional[bool]

    #: Indicates if the analyzed record has a valid geometry
    isValid: Optional[bool]

    #: if invalid geometry, display the Error message
    validationError: Optional[str]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "name": "SpatialBoundingAnalysis",
        "fields": [
            {
                "name": "spatialBoundingExists",
                "type": [
                    "null",
                    "boolean"
                ],
                "default": null,
                "doc": "Indicates if the analyzed record has a spatial bounding"
            },
            {
                "name": "isValid",
                "type": [
                    "null",
                    "boolean"
                ],
                "default": null,
                "doc": "Indicates if the analyzed record has a valid geometry"
            },
            {
                "name": "validationError",
                "type": [
                    "null",
                    "string"
                ],
                "default": null,
                "doc": "if invalid geometry, display the Error message"
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
    ) -> 'SpatialBoundingAnalysis':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
