from dataclasses import dataclass, asdict
import uuid


@dataclass
class Permission:
    id: uuid.UUID
    name: str 

