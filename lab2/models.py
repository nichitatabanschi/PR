from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    offer_type = db.Column(db.String(50))
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    generation = db.Column(db.String(50))
    registration = db.Column(db.String(50))
    condition = db.Column(db.String(50))
    country_origin = db.Column(db.String(50))
    manufacturing_year = db.Column(db.String(4))
    price = db.Column(db.Integer)
    currency = db.Column(db.String(3))
    mileage = db.Column(db.String(50))
    engine_capacity = db.Column(db.String(50))
    power_hp = db.Column(db.Integer)
    fuel_type = db.Column(db.String(50))
    transmission = db.Column(db.String(50))
    color = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.id,
            "offer_type": self.offer_type,
            "brand": self.brand,
            "model": self.model,
            "generation": self.generation,
            "registration": self.registration,
            "condition": self.condition,
            "country_origin": self.country_origin,
            "manufacturing_year": self.manufacturing_year,
            "price": self.price,
            "currency": self.currency,
            "mileage": self.mileage,
            "engine_capacity": self.engine_capacity,
            "power_hp": self.power_hp,
            "fuel_type": self.fuel_type,
            "transmission": self.transmission,
            "color": self.color
        }
    ##