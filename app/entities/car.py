from dataclasses import dataclass, asdict
import uuid


@dataclass
class Car:
    id: uuid.UUID
    brand: str
    model: str
    model_year: int


