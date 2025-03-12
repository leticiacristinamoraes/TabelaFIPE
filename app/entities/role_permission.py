from dataclasses import dataclass, asdict
import uuid


@dataclass
class RolePermission:
    id: uuid.UUID
    role_id: uuid.UUID
    permission_id: uuid.UUID

    @classmethod
    def from_dict(cls, data):
        """ Convert data from a dictionary
        """
        return cls(**data)

    def to_dict(self):
        """ Convert data into dictionary
        """
        return asdict(self)