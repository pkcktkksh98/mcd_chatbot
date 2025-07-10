from db.database import SessionLocal, engine
from db.models import Base, McdOutlet
from sqlalchemy.exc import IntegrityError

Base.metadata.create_all(bind=engine)

def save_outlets_to_db(store_data):
    db = SessionLocal()

    # Optional: Clear existing data before insert
    db.query(McdOutlet).delete()
    db.commit()

    for store in store_data:
        try:
            # Handle features: convert list to string if needed
            raw_features = store.get("features", [])
            features = ", ".join(raw_features) if isinstance(raw_features, list) else str(raw_features)

            new_outlet = McdOutlet(
                name=str(store.get("name", "")).strip(),
                address=str(store.get("address", "")).strip(),
                lat=float(store.get("latitude", 0.0)),
                lng=float(store.get("longitude", 0.0)),
                state=str(store.get("state", "")).strip(),
                telephone=str(store.get("phone", "")).strip(),
                fax=str(store.get("fax", "")).strip(),
                hours=str(store.get("hours", "")).strip(),
                features=features,
                waze_link=str(store.get("waze_link", "")).strip(),
                # Optional: Add Google Maps if needed
                # google_maps=f"https://www.google.com/maps?q={store.get('latitude')},{store.get('longitude')}",
            )

            db.add(new_outlet)
            db.commit()
            print(f"✅ Inserted: {new_outlet.name}")
        except IntegrityError:
            db.rollback()
            print(f"❌ Skipped (IntegrityError): {store.get('name')}")

    db.close()
    print("🎉 All data saved to DB.")
