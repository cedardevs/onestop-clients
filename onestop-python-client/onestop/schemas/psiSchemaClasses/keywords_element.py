from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, List, Optional

from undictify import type_checked_constructor


@type_checked_constructor()
@dataclass
class KeywordsElement:
    values: List[str]
    type: Optional[str]
    namespace: Optional[str]

    #: The Avro Schema associated to this class
    _schema: ClassVar[str] = """{
        "name": "KeywordsElement",
        "type": "record",
        "fields": [
            {
                "name": "values",
                "type": {
                    "type": "array",
                    "items": "string"
                },
                "default": []
            },
            {
                "name": "type",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
            },
            {
                "name": "namespace",
                "type": [
                    "null",
                    "string"
                ],
                "default": null
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
    ) -> 'KeywordsElement':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
