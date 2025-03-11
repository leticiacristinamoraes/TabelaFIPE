from dataclasses import dataclass, asdict
import uuid


@dataclass
class RolePermission:
    id: uuid.UUID
    role_id: uuid.UUID
    permission_id: uuid.UUID