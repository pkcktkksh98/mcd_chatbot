from db.database import SessionLocal, engine
from db.models import Base, McdOutlet
from sqlalchemy.exc import IntegrityError
from utils.state_extractor import extract_state_from_address

Base.metadata.create_all(bind=engine)

# Save to DB
def save_outlets_to_db(store_data):
    db = SessionLocal()
    db.query(McdOutlet).delete()
    db.commit()

    for store in store_data:
        name = store["name"]
        address = store["address"]
        lat = float(store["lat"])
        lng = float(store["lng"])
        state = extract_state_from_address(address)
        waze_link = f"https://waze.com/ul?ll={lat},{lng}&navigate=yes"
        google_maps = f"https://www.google.com/maps?q={lat},{lng}"
        categories = [cat["cat_name"] for cat in store.get("cat", [])]
        features = ", ".join(categories)

        new_outlet = McdOutlet(
            name=name,
            address=address,
            telephone=store.get("telephone", ""),
            email=store.get("email", ""),
            lat=lat,
            lng=lng,
            state=state,
            features=features,
            waze_link=waze_link,
            google_maps=google_maps
        )

        try:
            db.add(new_outlet)
            db.commit()
            print(f"✅ Inserted: {name}")
        except IntegrityError:
            db.rollback()
            print(f"❌ Skipped (IntegrityError): {name}")

    db.close()
    print("🎉 All data saved to DB.")

