from enum import Enum
from typing import ClassVar


class RelationshipType(Enum):
    """
    The types of metadata relationships which can be represented in the PSI system
    """
    collection = 'COLLECTION'

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "RelationshipType",
        "namespace": "org.cedar.schemas.avro.psi",
        "type": "enum",
        "doc": "
        "symbols": [
            "COLLECTION"
        ]
    }"""
