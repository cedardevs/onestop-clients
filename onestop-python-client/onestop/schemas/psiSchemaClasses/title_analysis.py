from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional

from undictify import type_checked_constructor


@type_checked_constructor()
@dataclass
class TitleAnalysis:
    #: Indicates if the analyzed record has a title
    titleExists: Optional[bool]

    #: The number of characters in the analyzed record's title
    titleCharacters: Optional[int]

    #: Indicates if the analyzed record has an alternate title
    alternateTitleExists: Optional[bool]

    #: The number of characters in the analyzed record's alternate title
    alternateTitleCharacters: Optional[int]

    #: Flesch reading-ease score measuring the reading ease of the record's title
    titleFleschReadingEaseScore: Optional[float]

    #: Flesch reading-ease score measuring the reading ease of the record's alternate title
    alternateTitleFleschReadingEaseScore: Optional[float]

    #: Flesch-Kincaid readability test grade level presenting the U.S. grade level, or approximate years of education required to understand the record's title
    titleFleschKincaidReadingGradeLevel: Optional[float]

    #: Flesch-Kincaid readability test grade level presenting the U.S. grade level, or approximate years of education required to understand the record's alternate title
    alternateTitleFleschKincaidReadingGradeLevel: Optional[float]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "name": "TitleAnalysis",
        "fields": [
            {
                "name": "titleExists",
                "type": [
                    "null",
                    "boolean"
                ],
                "default": null,
                "doc": "Indicates if the analyzed record has a title"
            },
            {
                "name": "titleCharacters",
                "type": [
                    "null",
                    "int"
                ],
                "default": null,
                "doc": "The number of characters in the analyzed record's title"
            },
            {
                "name": "alternateTitleExists",
                "type": [
                    "null",
                    "boolean"
                ],
                "default": null,
                "doc": "Indicates if the analyzed record has an alternate title"
            },
            {
                "name": "alternateTitleCharacters",
                "type": [
                    "null",
                    "int"
                ],
                "default": null,
                "doc": "The number of characters in the analyzed record's alternate title"
            },
            {
                "name": "titleFleschReadingEaseScore",
                "type": [
                    "null",
                    "double"
                ],
                "default": null,
                "doc": "Flesch reading-ease score measuring the reading ease of the record's title"
            },
            {
                "name": "alternateTitleFleschReadingEaseScore",
                "type": [
                    "null",
                    "double"
                ],
                "default": null,
                "doc": "Flesch reading-ease score measuring the reading ease of the record's alternate title"
            },
            {
                "name": "titleFleschKincaidReadingGradeLevel",
                "type": [
                    "null",
                    "double"
                ],
                "default": null,
                "doc": "Flesch-Kincaid readability test grade level presenting the U.S. grade level, or approximate years of education required to understand the record's title"
            },
            {
                "name": "alternateTitleFleschKincaidReadingGradeLevel",
                "type": [
                    "null",
                    "double"
                ],
                "default": null,
                "doc": "Flesch-Kincaid readability test grade level presenting the U.S. grade level, or approximate years of education required to understand the record's alternate title"
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
    ) -> 'TitleAnalysis':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
