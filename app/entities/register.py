from dataclasses import dataclass, asdict
import datetime
import uuid

@dataclass
class Register:
    id: uuid.UUID
    car_id: uuid
    shop_id: uuid 
    price: str
    created_date: datetime.datetime