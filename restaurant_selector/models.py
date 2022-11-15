
from sqlalchemy import Boolean, Column, Integer, String
from restaurant_selector.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    tags = Column(String(100))
    quick_take_away = Column(Boolean, default=False)
    emoji = Column(String(100), default = '')
