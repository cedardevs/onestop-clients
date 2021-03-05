from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, List

from undictify import type_checked_constructor

from onestop.schemas.geojsonSchemaClasses.point_type import PointType


@type_checked_constructor()
@dataclass
class Point:
    """
    A single position described with two values: longitude then latitude. A third (optional) value for elevation is allowed.
    """
    type: PointType
    coordinates: List[float]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "name": "Point",
        "doc": "A single position described with two values: longitude then latitude. A third (optional) value for elevation is allowed.",
        "namespace": "org.cedar.schemas.avro.geojson",
        "fields": [
            {
                "name": "type",
                "type": {
                    "name": "PointType",
                    "type": "enum",
                    "symbols": [
                        "Point"
                    ]
                },
                "default": "Point"
            },
            {
                "name": "coordinates",
                "type": {
                    "type": "array",
                    "items": "double"
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
    ) -> 'Point':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
