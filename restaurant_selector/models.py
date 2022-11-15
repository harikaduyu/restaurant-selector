
from sqlalchemy import Boolean, Column, Integer, String, SmallInteger
from restaurant_selector.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    cuisine = Column(String(100))
    take_away = Column(Boolean, default=False)
    # emoji = Column(String(100), default = '')
    email = Column(String(100))
    indoor_seating = Column(Boolean, default=True)
    level = Column(SmallInteger)
    opening_hours = Column(String(100))
    outdoor_seating = Column(Boolean, default=False)
    payment_mastercard = Column(Boolean, default=False)
    payment_visa = Column(Boolean, default=False)
    phone = Column(String(100))
    website = Column(String(150))
    wheelchair = Column(Boolean, default=False)
    smoking = Column(String(50))
    diet_vegan = Column(String(50))
    diet_vegetarian = Column(String(50))
