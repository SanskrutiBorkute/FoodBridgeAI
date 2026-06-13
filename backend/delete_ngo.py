from database import SessionLocal
from models import NGO

db = SessionLocal()

ngo = db.query(NGO).filter(NGO.id == 2).first()

if ngo:
    db.delete(ngo)
    db.commit()
    print("Deleted NGO ID 2")
else:
    print("NGO not found")

db.close()
