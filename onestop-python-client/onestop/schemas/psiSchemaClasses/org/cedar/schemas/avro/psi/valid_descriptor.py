from dataclasses import asdict, dataclass
from typing import Dict

from undictify import type_checked_constructor


@type_checked_constructor()
@dataclass
class ValidDescriptor:
    def to_dict(self) -> Dict:
        """
        Returns a dictionary version of this instance.
        """
        return asdict(self)

    @classmethod
    def from_dict(
            cls,
            the_dict: Dict
    ) -> 'ValidDescriptor':
        """
        Returns an instance of this class from a dictionary.

        :param the_dict: The dictionary from which to create an instance of this class.
        """
        return cls(**the_dict)
