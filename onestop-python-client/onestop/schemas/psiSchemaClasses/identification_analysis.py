from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional

from undictify import type_checked_constructor


@type_checked_constructor()
@dataclass
class IdentificationAnalysis:
    #: Indicates if the analyzed record has a file identifier
    fileIdentifierExists: Optional[bool]

    #: The value of the analyzed record's file identifier, if present
    fileIdentifierString: Optional[str]

    #: Indicates if the analyzed record has a Digital Object Identifier
    doiExists: Optional[bool]

    #: The value of the analyzed record's Digital Object Identifier, if present
    doiString: Optional[str]

    #: Indicates if the analyzed record has a parent identifier
    parentIdentifierExists: Optional[bool]

    #: The value of the analyzed record's parent identifier, if present
    parentIdentifierString: Optional[str]

    #: Indicates if the analyzed record has a hierarchy level name
    hierarchyLevelNameExists: Optional[bool]

    #: Resolves to true if metadata content indicates a record is a granule. That is, a parent identifier is present and the hierarchy level name is 'granule'.
    isGranule: Optional[bool]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "name": "IdentificationAnalysis",
        "fields": [
            {
                "name": "fileIdentifierExists",
                "type": [
                    "null",
                    "boolean"
                ],
                "default": null,
                "doc": "Indicates if the analyzed record has a file identifier"
            },
            {
                "name": "fileIdentifierString",
                "type": [
                    "null",
                    "string"
                ],
                "default": null,
                "doc": "The value of the analyzed record's file identifier, if present"
            },
            {
                "name": "doiExists",
                "type": [
                    "null",
                    "boolean"
                ],
                "default": null,
                "doc": "Indicates if the analyzed record has a Digital Object Identifier"
            },
            {
                "name": "doiString",
                "type": [
                    "null",
                    "string"
                ],
                "default": null,
                "doc": "The value of the analyzed record's Digital Object Identifier, if present"
            },
            {
                "name": "parentIdentifierExists",
                "type": [
                    "null",
                    "boolean"
                ],
                "default": null,
                "doc": "Indicates if the analyzed record has a parent identifier"
            },
            {
                "name": "parentIdentifierString",
                "type": [
                    "null",
                    "string"
                ],
                "default": null,
                "doc": "The value of the analyzed record's parent identifier, if present"
            },
            {
                "name": "hierarchyLevelNameExists",
                "type": [
                    "null",
                    "boolean"
                ],
                "default": null,
                "doc": "Indicates if the analyzed record has a hierarchy level name"
            },
            {
                "name": "isGranule",
                "type": [
                    "null",
                    "boolean"
                ],
                "default": null,
                "doc": "Resolves to true if metadata content indicates a record is a granule. That is, a parent identifier is present and the hierarchy level name is 'granule'."
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
    ) -> 'IdentificationAnalysis':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
