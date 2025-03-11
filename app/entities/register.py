from dataclasses import dataclass, asdict
import datetime
import uuid

@dataclass
class Register:
    id: uuid.UUID
    car_id: uuid.UUID
    shop_id: uuid.UUID
    price: str
    created_date: datetime.datetime