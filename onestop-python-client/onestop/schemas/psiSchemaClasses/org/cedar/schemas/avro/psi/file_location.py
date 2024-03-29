from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Optional

from undictify import type_checked_constructor

from .file_location_type import FileLocationType


@type_checked_constructor()
@dataclass
class FileLocation:
    """
    A location at which a file is stored and/or available. All locations require a URI and the equality of two locations is defined by the equality of their URIs
    """

    #: A Uniform Resource Identifier as defined by RFCs 2396 and 3986
    uri: str

    #: The type of the file location, e.g. an ingest location, access location, etc.
    type: Optional[FileLocationType]

    #: Indicates if the file has been deleted from this location. Allows for preservation of previously-active locations, for example
    deleted: bool

    #: Is access to this location restricted from the public?
    restricted: bool

    #: Indicates if access to this location is asynchronous, e.g. it is stored in a tape library
    asynchronous: bool

    #: A string indicating the locality of the data, e.g. a FISMA boundary, an AWS Region, an archive service, etc.
    locality: Optional[str]

    #: The datetime at which this location was created or last modified, whichever is more recent, stored as the number of milliseconds from the unix epoch
    lastModified: Optional[int]

    #: The type of service this location belongs to, e.g. Amazon:AWS:S3 or OGC:CSW. These should be valid values for srv:serviceType or gmd:protocol attributes in ISO-19115 metadata
    serviceType: Optional[str]

    #: A discretionary map of key/value pairs to capture arbitrary attributes
    optionalAttributes: Dict[str, str]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "namespace": "org.cedar.schemas.avro.psi",
        "name": "FileLocation",
        "doc": "A location at which a file is stored and/or available. All locations require a URI and the equality of two locations is defined by the equality of their URIs",
        "fields": [
            {
                "name": "uri",
                "type": "string",
                "doc": "A Uniform Resource Identifier as defined by RFCs 2396 and 3986"
            },
            {
                "name": "type",
                "type": [
                    "null",
                    "org.cedar.schemas.avro.psi.FileLocationType"
                ],
                "doc": "The type of the file location, e.g. an ingest location, access location, etc.",
                "default": null
            },
            {
                "name": "deleted",
                "type": "boolean",
                "doc": "Indicates if the file has been deleted from this location. Allows for preservation of previously-active locations, for example",
                "default": false
            },
            {
                "name": "restricted",
                "type": "boolean",
                "doc": "Is access to this location restricted from the public?",
                "default": false
            },
            {
                "name": "asynchronous",
                "type": "boolean",
                "doc": "Indicates if access to this location is asynchronous, e.g. it is stored in a tape library",
                "default": false
            },
            {
                "name": "locality",
                "type": [
                    "null",
                    "string"
                ],
                "doc": "A string indicating the locality of the data, e.g. a FISMA boundary, an AWS Region, an archive service, etc.",
                "default": null
            },
            {
                "name": "lastModified",
                "type": [
                    "null",
                    "long"
                ],
                "doc": "The datetime at which this location was created or last modified, whichever is more recent, stored as the number of milliseconds from the unix epoch",
                "default": null
            },
            {
                "name": "serviceType",
                "type": [
                    "null",
                    "string"
                ],
                "doc": "The type of service this location belongs to, e.g. Amazon:AWS:S3 or OGC:CSW. These should be valid values for srv:serviceType or gmd:protocol attributes in ISO-19115 metadata",
                "default": null
            },
            {
                "name": "optionalAttributes",
                "type": {
                    "type": "map",
                    "values": "string"
                },
                "doc": "A discretionary map of key/value pairs to capture arbitrary attributes",
                "default": {}
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
    ) -> 'FileLocation':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
