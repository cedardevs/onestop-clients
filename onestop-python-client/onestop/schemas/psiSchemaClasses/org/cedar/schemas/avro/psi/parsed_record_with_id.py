from dataclasses import asdict, dataclass
from typing import ClassVar, Dict

from undictify import type_checked_constructor

from .parsed_record import ParsedRecord


@type_checked_constructor()
@dataclass
class ParsedRecordWithId:
    """
    A wrapper to tie a ParsedRecord together with an ID
    """

    #: The id string to be associated with the record
    id: str

    #: The ParsedRecord object to be associated with the id
    record: ParsedRecord

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "type": "record",
        "namespace": "org.cedar.schemas.avro.psi",
        "name": "ParsedRecordWithId",
        "doc": "A wrapper to tie a ParsedRecord together with an ID",
        "fields": [
            {
                "name": "id",
                "type": "string",
                "doc": "The id string to be associated with the record"
            },
            {
                "name": "record",
                "type": "org.cedar.schemas.avro.psi.ParsedRecord",
                "doc": "The ParsedRecord object to be associated with the id"
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
    ) -> 'ParsedRecordWithId':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
