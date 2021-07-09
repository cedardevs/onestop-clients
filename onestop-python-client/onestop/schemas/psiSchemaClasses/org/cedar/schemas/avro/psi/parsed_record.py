from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, List, Optional

from undictify import type_checked_constructor


from .discovery import Discovery
from .error_event import ErrorEvent
from .file_information import FileInformation
from .file_location import FileLocation
from .publishing import Publishing
from .record_type import RecordType
from .relationship import Relationship
from .analysis import Analysis



@type_checked_constructor()
@dataclass
class ParsedRecord:
    type: Optional[RecordType]
    discovery: Optional[Discovery]
    analysis: Optional[Analysis]

    #: Details about the file that this input object is in reference to
    fileInformation: Optional[FileInformation]

    #: A list of location objects describing where the file is located
    fileLocations: Dict[str, FileLocation]
    publishing: Optional[Publishing]

    #: A record of this objects relationships to other objects in the inventory
    relationships: Optional[List[Relationship]]
    errors: Optional[List[ErrorEvent]]

        #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "namespace": "org.cedar.schemas.avro.psi",
        "name": "ParsedRecord",
        "doc": "",
        "fields": [
            {
                "name": "type",
                "type": [
                    "null",
                    "org.cedar.schemas.avro.psi.RecordType"
                ],
                "default": null
            },
            {
                "name": "discovery",
                "type": [
                    "null",
                    "org.cedar.schemas.avro.psi.Discovery"
                ],
                "default": null
            },
            {
                "name": "analysis",
                "type": [
                    "null",
                    "org.cedar.schemas.avro.psi.Analysis"
                ],
                "default": null
            },
            {
                "name": "fileInformation",
                "type": [
                    "null",
                    "org.cedar.schemas.avro.psi.FileInformation"
                ],
                "doc": "Details about the file that this input object is in reference to",
                "default": null
            },
            {
                "name": "fileLocations",
                "type": {
                    "type": "map",
                    "values": "org.cedar.schemas.avro.psi.FileLocation"
                },
                "doc": "A list of location objects describing where the file is located",
                "default": {}
            },
            {
                "name": "publishing",
                "type": "org.cedar.schemas.avro.psi.Publishing",
                "default": {
                    "isPrivate": false,
                    "until": null
                }
            },
            {
                "name": "relationships",
                "type": {
                    "type": "array",
                    "items": "org.cedar.schemas.avro.psi.Relationship"
                },
                "doc": "A record of this objects relationships to other objects in the inventory",
                "default": []
            },
            {
                "name": "errors",
                "type": {
                    "type": "array",
                    "items": "org.cedar.schemas.avro.psi.ErrorEvent"
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
    ) -> 'ParsedRecord':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
