from enum import Enum
from typing import ClassVar


class RecordType(Enum):
    """
    The types of metadata records which can be represented in the PSI system
    """
    collection = 'collection'
    granule = 'granule'

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "RecordType",
        "namespace": "org.cedar.schemas.avro.psi",
        "type": "enum",
        "doc": "The types of metadata records which can be represented in the PSI system",
        "symbols": [
            "collection",
            "granule"
        ]
    }"""
