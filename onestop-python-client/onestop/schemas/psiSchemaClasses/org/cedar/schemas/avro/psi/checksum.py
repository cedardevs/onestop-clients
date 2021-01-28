from dataclasses import asdict, dataclass
from typing import ClassVar, Dict

from undictify import type_checked_constructor

from .checksum_algorithm import ChecksumAlgorithm


@type_checked_constructor()
@dataclass
class Checksum:
    algorithm: ChecksumAlgorithm
    ## algorithm: str
    value: str

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "Checksum",
        "namespace": "org.cedar.schemas.avro.psi",
        "type": "record",
        "fields": [
            {
                "name": "algorithm",
                "type": "org.cedar.schemas.avro.psi.ChecksumAlgorithm"
            },
            {
                "name": "value",
                "type": "string"
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
    ) -> 'Checksum':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
