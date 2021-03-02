from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, List, Union

from undictify import type_checked_constructor

from onestop.schemas.geojsonSchemaClasses.line_string_type import LineStringType


@type_checked_constructor()
@dataclass
class LineString:
    """
    An array of two or more CONNECTED positions, each described with two values: longitude then latitude. A third (optional) value for elevation is allowed per position. A LineString may self-cross.
    """
    type: LineStringType
    coordinates: List[Union[List[float]]]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "name": "LineString",
        "doc": "An array of two or more CONNECTED positions, each described with two values: longitude then latitude. A third (optional) value for elevation is allowed per position. A LineString may self-cross.",
        "namespace": "org.cedar.schemas.avro.geojson",
        "fields": [
            {
                "name": "type",
                "type": {
                    "name": "LineStringType",
                    "type": "enum",
                    "symbols": [
                        "LineString"
                    ]
                },
                "default": "LineString"
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
    ) -> 'LineString':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
