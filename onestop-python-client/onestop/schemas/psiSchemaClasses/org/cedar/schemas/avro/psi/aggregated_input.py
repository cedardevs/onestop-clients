from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, List, Optional

from undictify import type_checked_constructor

from .error_event import ErrorEvent
from .file_information import FileInformation
from .file_location import FileLocation
from .input_event import InputEvent
from .publishing import Publishing
from .record_type import RecordType
from .relationship import Relationship


@type_checked_constructor()
@dataclass
class AggregatedInput:
    """
    The aggregated most recent view for a metadata record. Raw input is maintained but some high-level inventory management data is extracted, when known, at this point.
    """

    #: The raw aggregated JSON input content as a string
    rawJson: Optional[str]

    #: The raw most recent XML input content as a string
    rawXml: Optional[str]

    #: The initial source of the input, e.g. the name of an external system which first provided this input record
    initialSource: Optional[str]

    #: The type of record represented by this input
    type: Optional[RecordType]

    #: Details about the file that this input object is in reference to
    fileInformation: Optional[FileInformation]

    #: A map of URIs to location objects describing where the file is located
    fileLocations: Dict[str, FileLocation]

    #: Information pertaining to whether a file is private and for how long if so
    publishing: Optional[Publishing]

    #: A record of this objects relationships to other objects in the inventory
    relationships: List[Relationship]

    #: Whether or not this input should be treated as deleted downstream
    deleted: bool

    #: A list of each instance where modifications to this input object were received
    events: List[InputEvent]

    #: A list of any errors that may have been encountered between receiving input events for this object and consolidating all events into this aggregated object
    errors: List[ErrorEvent]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "namespace": "org.cedar.schemas.avro.psi",
        "name": "AggregatedInput",
        "doc": "The aggregated most recent view for a metadata record. Raw input is maintained but some high-level inventory management data is extracted, when known, at this point.",
        "fields": [
            {
                "name": "rawJson",
                "type": [
                    "null",
                    "string"
                ],
                "doc": "The raw aggregated JSON input content as a string",
                "default": null
            },
            {
                "name": "rawXml",
                "type": [
                    "null",
                    "string"
                ],
                "doc": "The raw most recent XML input content as a string",
                "default": null
            },
            {
                "name": "initialSource",
                "type": [
                    "null",
                    "string"
                ],
                "doc": "The initial source of the input, e.g. the name of an external system which first provided this input record",
                "default": null
            },
            {
                "name": "type",
                "type": [
                    "null",
                    "org.cedar.schemas.avro.psi.RecordType"
                ],
                "doc": "The type of record represented by this input",
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
                "doc": "A map of URIs to location objects describing where the file is located",
                "default": {}
            },
            {
                "name": "publishing",
                "type": [
                    "null",
                    "org.cedar.schemas.avro.psi.Publishing"
                ],
                "doc": "Information pertaining to whether a file is private and for how long if so",
                "default": null
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
                "name": "deleted",
                "type": "boolean",
                "doc": "Whether or not this input should be treated as deleted downstream",
                "default": false
            },
            {
                "name": "events",
                "type": {
                    "type": "array",
                    "items": "org.cedar.schemas.avro.psi.InputEvent"
                },
                "doc": "A list of each instance where modifications to this input object were received",
                "default": []
            },
            {
                "name": "errors",
                "type": {
                    "type": "array",
                    "items": "org.cedar.schemas.avro.psi.ErrorEvent"
                },
                "doc": "A list of any errors that may have been encountered between receiving input events for this object and consolidating all events into this aggregated object",
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
    ) -> 'AggregatedInput':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
