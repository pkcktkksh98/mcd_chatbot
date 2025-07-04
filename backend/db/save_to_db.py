from db.database import SessionLocal, engine
from db.models import Base, McdOutlet
from sqlalchemy.exc import IntegrityError

Base.metadata.create_all(bind=engine)

def save_outlets(outlets):
    db = SessionLocal()
    db.query(McdOutlet).delete()
    db.commit()

    # 💾 Insert new outlets
    for outlet in outlets:
        new_outlet = McdOutlet(
            name=outlet["name"],
            address=outlet["address"],
            waze_link=outlet.get("waze_link"),
            hours=outlet.get("hours"),
            latitude=outlet.get("latitude"),
            longitude=outlet.get("longitude"),
        )
        try:
            print(f"Inserted: {outlet['name']}")
            db.add(new_outlet)
            db.commit()
        except IntegrityError:
            db.rollback()

    db.commit()
    db.close()
