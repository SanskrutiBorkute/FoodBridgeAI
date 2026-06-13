from pydantic import BaseModel

class DonationCreate(BaseModel):
    restaurant_name: str
    food_type: str
    quantity: int
    location: str
    expiry_hours: int
    
class NGOCreate(BaseModel):
    name: str
    location: str
    capacity: int
    vehicles: int
