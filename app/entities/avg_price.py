from dataclasses import dataclass, asdict
import datetime
import uuid
@dataclass
class AvgPrice:
    id: uuid.UUID
    car_id: str
    avg_price: str
    
    @classmethod
    def from_dict(cls, data):
        """ Convert data from a dictionary
        """
        return cls(**data)

    def to_dict(self):
        """ Convert data into dictionary
        """
        return asdict(self)