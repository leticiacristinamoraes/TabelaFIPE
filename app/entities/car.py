from dataclasses import dataclass, asdict
import uuid


@dataclass
class Car:
    id: uuid.UUID
    model_id: uuid.UUID
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

@dataclass
class Model:
    id: uuid.UUID
    name: str
    brand_id: uuid.UUID
    
    @classmethod
    def from_dict(cls, data):
        """ Convert data from a dictionary
        """
        return cls(**data)

    def to_dict(self):
        """ Convert data into dictionary
        """
        return asdict(self)
    
@dataclass
class Brand:
    id: uuid.UUID
    name: str
    
    @classmethod
    def from_dict(cls, data):
        """ Convert data from a dictionary
        """
        return cls(**data)

    def to_dict(self):
        """ Convert data into dictionary
        """
        return asdict(self)