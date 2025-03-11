from dataclasses import dataclass, asdict
import uuid


@dataclass
class Role:
    id: uuid.UUID
    name: str 