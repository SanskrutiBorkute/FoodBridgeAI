from fastapi import FastAPI
from database import engine, Base, SessionLocal
from schemas import DonationCreate, NGOCreate
from models import Donation, NGO
from ai_engine import calculate_priority
from fastapi.middleware.cors import CORSMiddleware
import models
import joblib
import numpy as np

priority_model = joblib.load("priority_model.pkl")
forecast_model = joblib.load("forecast_model.pkl")

app = FastAPI(
    title="FoodBridge AI",
    description="AI Powered Food Waste Redistribution System",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "project": "FoodBridge AI",
        "status": "Running Successfully"
    }


@app.post("/donation")
def create_donation(data: DonationCreate):

    db = SessionLocal()

    priority = int(
    priority_model.predict(
        np.array([
            [
                data.quantity,
                data.expiry_hours
            ]
        ])
    )[0]
)

    donation = Donation(
        restaurant_name=data.restaurant_name,
        food_type=data.food_type,
        quantity=data.quantity,
        location=data.location,
        expiry_hours=data.expiry_hours,
        priority_score=priority
    )

    db.add(donation)
    db.commit()
    db.refresh(donation)

    db.close()

    return {
        "message": "Donation Added Successfully",
        "priority_score": priority,
        "donation_id": donation.id
    }

@app.get("/donations")
def get_donations():

    db = SessionLocal()

    donations = db.query(Donation).order_by(
        Donation.priority_score.desc()
    ).all()

    result = []

    for donation in donations:
        result.append({
            "id": donation.id,
            "restaurant_name": donation.restaurant_name,
            "food_type": donation.food_type,
            "quantity": donation.quantity,
            "location": donation.location,
            "expiry_hours": donation.expiry_hours,
            "priority_score": donation.priority_score,
            "assigned_ngo": donation.assigned_ngo,
            "status": donation.status
        })

    db.close()

    return result

@app.post("/ngo")
def create_ngo(data: NGOCreate):

    db = SessionLocal()

    ngo = NGO(
        name=data.name,
        location=data.location,
        capacity=data.capacity,
        vehicles=data.vehicles
    )

    db.add(ngo)
    db.commit()
    db.refresh(ngo)

    db.close()

    return {
        "message": "NGO Added Successfully",
        "ngo_id": ngo.id
    }


@app.get("/ngos")
def get_ngos():

    db = SessionLocal()

    ngos = db.query(NGO).all()

    result = []

    for ngo in ngos:
        result.append({
            "id": ngo.id,
            "name": ngo.name,
            "location": ngo.location,
            "capacity": ngo.capacity,
            "vehicles": ngo.vehicles
        })

    db.close()
    return result

@app.get("/delete_duplicate")
def delete_duplicate():

    db = SessionLocal()

    ngo = db.query(NGO).filter(
        NGO.id == 2
    ).first()

    if ngo:
        db.delete(ngo)
        db.commit()

    db.close()

    return {"message": "Duplicate NGO deleted"}

@app.put("/assign/{donation_id}")
def assign_donation(donation_id: int):

    db = SessionLocal()

    donation = db.query(Donation).filter(
        Donation.id == donation_id
    ).first()

    if not donation:
        db.close()
        return {"error": "Donation not found"}

    ngos = db.query(NGO).all()

    if not ngos:
        db.close()
        return {"error": "No NGOs available"}

    best_score = -1
    best_ngo = None

    for ngo in ngos:
        capacity_score = min(
            ngo.capacity / donation.quantity,
            1
        ) * 60

        vehicle_score = min(
            ngo.vehicles,
            5
        ) * 8

        urgency_bonus = max(
            0,
            (24 - donation.expiry_hours)
        ) * 0.5

        total_score = (
            capacity_score +
            vehicle_score +
            urgency_bonus
        )

        if total_score > best_score:
            best_score = total_score
            best_ngo = ngo

    if best_ngo is None:
        db.close()
        return {"error": "No suitable NGO found"}

    donation.assigned_ngo = best_ngo.name
    donation.status = "Assigned"

    ngo_name = best_ngo.name
    match_score = round(best_score)

    db.commit()
    db.close()

    print("MATCH SCORE =", match_score)
    
    return {
        "message": "Donation Assigned",
        "ngo": ngo_name,
        "match_score": match_score
    }

@app.put("/pickup/{donation_id}")
def pickup_donation(donation_id: int):

    db = SessionLocal()

    donation = db.query(Donation).filter(
        Donation.id == donation_id
    ).first()

    if not donation:
        db.close()
        return {"error": "Donation not found"}

    donation.status = "Picked Up"

    db.commit()
    db.close()
    return {
        "message": "Donation Picked Up"
    }


@app.put("/deliver/{donation_id}")
def deliver_donation(donation_id: int):

    db = SessionLocal()

    donation = db.query(Donation).filter(
        Donation.id == donation_id
    ).first()

    if not donation:
        db.close()
        return {"error": "Donation not found"}

    donation.status = "Delivered"

    db.commit()
    db.close()
    return {
        "message": "Donation Delivered"
    }

@app.get("/forecast")
def get_forecast():

    db = SessionLocal()

    ngos = db.query(NGO).all()

    result = []

    total = 0

    for ngo in ngos:

        predicted = int(
            forecast_model.predict(
                np.array([[ngo.capacity]])
            )[0]
        )

        total += predicted

        result.append({
            "ngo": ngo.name,
            "forecast": predicted
        })

    db.close()

    return {
        "forecasts": result,
        "total": total
    }