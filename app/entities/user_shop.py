from dataclasses import dataclass, asdict
import uuid


@dataclass
class UserShop:
    id: uuid.UUID
    user_id: uuid.UUID 
    shop_id: uuid.UUID

    @classmethod
    def from_dict(cls, data):
        """ Convert data from a dictionary
        """
        return cls(**data)

    def to_dict(self):
        """ Convert data into dictionary
        """
        return asdict(self)