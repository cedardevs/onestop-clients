from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional

from undictify import type_checked_constructor


@type_checked_constructor()
@dataclass
class ThumbnailAnalysis:
    #: Indicates if the analyzed record has a thumbnail
    thumbnailExists: Optional[bool]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "name": "ThumbnailAnalysis",
        "fields": [
            {
                "name": "thumbnailExists",
                "type": [
                    "null",
                    "boolean"
                ],
                "default": null,
                "doc": "Indicates if the analyzed record has a thumbnail"
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
    ) -> 'ThumbnailAnalysis':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
