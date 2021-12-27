from enum import Enum
from typing import ClassVar


class FileLocationType(Enum):
    INGEST = 'INGEST'
    ARCHIVE = 'ARCHIVE'
    ACCESS = 'ACCESS'
    WORKING = 'WORKING'

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "enum",
        "namespace": "org.cedar.schemas.avro.psi",
        "name": "FileLocationType",
        "doc": "The type of the file location, e.g. an ingest location, access location, etc.",
        "symbols": [
            "INGEST",
            "ARCHIVE",
            "ACCESS",
            "WORKING"
        ]
    }"""
