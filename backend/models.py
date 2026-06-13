from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


# -----------------------------
# Restaurants
# -----------------------------
class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    email = Column(String)
    phone = Column(String)

    location = Column(String)


# -----------------------------
# NGOs
# -----------------------------
class NGO(Base):
    __tablename__ = "ngos"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    location = Column(String)

    capacity = Column(Integer)

    vehicles = Column(Integer)


# -----------------------------
# Donations
# -----------------------------
class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)

    restaurant_name = Column(String)

    food_type = Column(String)

    quantity = Column(Integer)

    location = Column(String)

    expiry_hours = Column(Integer)

    priority_score = Column(Integer)

    assigned_ngo = Column(String, default="Not Assigned")

    status = Column(String, default="Pending")


# -----------------------------
# Pickups
# -----------------------------
class Pickup(Base):
    __tablename__ = "pickups"

    id = Column(Integer, primary_key=True, index=True)

    donation_id = Column(Integer)

    ngo_name = Column(String)

    pickup_status = Column(String)