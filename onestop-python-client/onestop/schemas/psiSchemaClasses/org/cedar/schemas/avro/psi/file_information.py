from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, List, Optional

from undictify import type_checked_constructor

from .checksum import Checksum


@type_checked_constructor()
@dataclass
class FileInformation:
    #: The file name
    name: str

    #: The size of the file in bytes
    size: int

    #: A list of checksums for the file
    checksums: List[Checksum]

    #: Optional field to indicate the format of the file
    format: Optional[str]

    #: Optional field to capture a file's headers
    headers: Optional[str]

    #: A discretionary map of key/value pairs to capture arbitrary attributes
    optionalAttributes: Dict[str, str]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "FileInformation",
        "namespace": "org.cedar.schemas.avro.psi",
        "type": "record",
        "fields": [
            {
                "name": "name",
                "doc": "The file name",
                "type": "string",
                "default": ""
            },
            {
                "name": "size",
                "doc": "The size of the file in bytes",
                "type": "long",
                "default": 0
            },
            {
                "name": "checksums",
                "doc": "A list of checksums for the file",
                "type": {
                    "type": "array",
                    "items": "org.cedar.schemas.avro.psi.Checksum"
                },
                "default": []
            },
            {
                "name": "format",
                "doc": "Optional field to indicate the format of the file",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "headers",
                "doc": "Optional field to capture a file's headers",
                "type": [
                    "null",
                    "string"
                ],
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
    ) -> 'FileInformation':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
