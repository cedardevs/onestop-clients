from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, List, Union

from undictify import type_checked_constructor

from onestop.schemas.geojsonSchemaClasses.multi_polygon_type import MultiPolygonType


@type_checked_constructor()
@dataclass
class MultiPolygon:
    """
    An array of separate polygons. A polygon is an array of linear rings, which are linestrings of four or more positions that are CLOSED, meaning the first and last positions are identical. The first (required) linear ring describes the polygon's exterior boundary. Subsequent (optional) linear rings describe holes in the polygon. Point positions MUST follow the right-hand rule for order, i.e., exterior rings are counterclockwise and holes are clockwise. Each point must be described with two values: longitude then latitude. A third (optional) value for elevation is allowed per position.
    """
    type: MultiPolygonType
    coordinates: List[Union[List[Union[List[Union[List[float]]]]]]]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "name": "MultiPolygon",
        "doc": "An array of separate polygons. A polygon is an array of linear rings, which are linestrings of four or more positions that are CLOSED, meaning the first and last positions are identical. The first (required) linear ring describes the polygon's exterior boundary. Subsequent (optional) linear rings describe holes in the polygon. Point positions MUST follow the right-hand rule for order, i.e., exterior rings are counterclockwise and holes are clockwise. Each point must be described with two values: longitude then latitude. A third (optional) value for elevation is allowed per position.",
        "namespace": "org.cedar.schemas.avro.geojson",
        "fields": [
            {
                "name": "type",
                "type": {
                    "name": "MultiPolygonType",
                    "type": "enum",
                    "symbols": [
                        "MultiPolygon"
                    ]
                },
                "default": "MultiPolygon"
            },
            {
                "name": "coordinates",
                "type": {
                    "type": "array",
                    "items": [
                        {
                            "type": "array",
                            "items": [
                                {
                                    "type": "array",
                                    "items": [
                                        {
                                            "type": "array",
                                            "items": "double"
                                        }
                                    ]
                                }
                            ]
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
    ) -> 'MultiPolygon':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
