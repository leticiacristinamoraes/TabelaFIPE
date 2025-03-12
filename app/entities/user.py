from dataclasses import dataclass, asdict
import uuid



userId = uuid.UUID
@dataclass
class User:
    id: userId
    name: str 
    email: str

    @classmethod
    def from_dict(cls, data):
        """ Convert data from a dictionary
        """
        return cls(**data)

    def to_dict(self):
        """ Convert data into dictionary
        """
        return asdict(self)