from dataclasses import dataclass, asdict
import uuid


@dataclass
class Shop:
    id: uuid.UUID
    name: str 