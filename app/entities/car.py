from dataclasses import dataclass, asdict
import uuid


@dataclass
class Car:
    id: uuid.UUID
    brand: str
    model: str
    model_year: int
    
    @classmethod
    def from_dict(cls, data):
        """ Convert data from a dictionary
        """
        return cls(**data)

    def to_dict(self):
        """ Convert data into dictionary
        """
        return asdict(self)

