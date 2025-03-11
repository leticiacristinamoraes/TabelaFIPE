from dataclasses import dataclass, asdict
import datetime
import uuid
@dataclass
class AvgPrice:
    id: uuid.UUID
    car_id: str
    avg_price: str
