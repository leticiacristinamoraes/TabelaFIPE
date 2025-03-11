from dataclasses import dataclass, asdict
import uuid


@dataclass
class UserRole:
    id: uuid.UUID
    user_id: uuid.UUID 
    role_id: uuid.UUID