from dataclasses import dataclass, asdict
import uuid


@dataclass
class User:
    id: uuid.UUID
    name: str 
    email: str

