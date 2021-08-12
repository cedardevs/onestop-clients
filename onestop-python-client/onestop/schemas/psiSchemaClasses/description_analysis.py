from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional

from undictify import type_checked_constructor


@type_checked_constructor()
@dataclass
class DescriptionAnalysis:
    #: Indicates if the analyzed record has a description
    descriptionExists: Optional[bool]

    #: The number of characters in the analyzed record's description
    descriptionCharacters: Optional[int]

    #: Flesch reading-ease score measuring the reading ease of the record's description
    descriptionFleschReadingEaseScore: Optional[float]

    #: Flesch-Kincaid readability test grade level presenting the U.S. grade level, or approximate years of education required to understand the record's description
    descriptionFleschKincaidReadingGradeLevel: Optional[float]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "name": "DescriptionAnalysis",
        "fields": [
            {
                "name": "descriptionExists",
                "type": [
                    "null",
                    "boolean"
                ],
                "default": null,
                "doc": "Indicates if the analyzed record has a description"
            },
            {
                "name": "descriptionCharacters",
                "type": [
                    "null",
                    "int"
                ],
                "default": null,
                "doc": "The number of characters in the analyzed record's description"
            },
            {
                "name": "descriptionFleschReadingEaseScore",
                "type": [
                    "null",
                    "double"
                ],
                "default": null,
                "doc": "Flesch reading-ease score measuring the reading ease of the record's description"
            },
            {
                "name": "descriptionFleschKincaidReadingGradeLevel",
                "type": [
                    "null",
                    "double"
                ],
                "default": null,
                "doc": "Flesch-Kincaid readability test grade level presenting the U.S. grade level, or approximate years of education required to understand the record's description"
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
    ) -> 'DescriptionAnalysis':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
