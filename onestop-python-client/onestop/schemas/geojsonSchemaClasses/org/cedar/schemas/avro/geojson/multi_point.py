from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, List, Union

from undictify import type_checked_constructor

from onestop.schemas.geojsonSchemaClasses.multi_point_type import MultiPointType


@type_checked_constructor()
@dataclass
class MultiPoint:
    """
    An array of UNCONNECTED positions, each described with two values: longitude then latitude. A third (optional) value for elevation is allowed per position.
    """
    type: MultiPointType
    coordinates: List[Union[List[float]]]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "name": "MultiPoint",
        "doc": "An array of UNCONNECTED positions, each described with two values: longitude then latitude. A third (optional) value for elevation is allowed per position.",
        "namespace": "org.cedar.schemas.avro.geojson",
        "fields": [
            {
                "name": "type",
                "type": {
                    "name": "MultiPointType",
                    "type": "enum",
                    "symbols": [
                        "MultiPoint"
                    ]
                },
                "default": "MultiPoint"
            },
            {
                "name": "coordinates",
                "type": {
                    "type": "array",
                    "items": [
                        {
                            "type": "array",
                            "items": "double"
                        }
                    ]
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
    ) -> 'MultiPoint':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
