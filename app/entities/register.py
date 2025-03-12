from dataclasses import dataclass, asdict
import datetime
import uuid

@dataclass
class Register:
    id: uuid.UUID
    car_id: uuid.UUID
    shop_id: uuid.UUID
    price: str
    created_date: datetime.datetime

    @classmethod
    def from_dict(cls, data):
        """ Convert data from a dictionary
        """
        return cls(**data)

    def to_dict(self):
        """ Convert data into dictionary
        """
        return asdict(self)