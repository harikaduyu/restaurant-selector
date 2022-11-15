import logging
from random import choice
from enum import Enum
from typing import List
import json

from fastapi import FastAPI, Depends, Request, Form, status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session

from restaurant_selector.database import SessionLocal, engine
import restaurant_selector.models as models

logger = logging.getLogger()
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
)


models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        set_up_database(db)
        yield db
    finally:
        db.close()




def set_up_database(db : Session = Depends(get_db)):
    restaurants = db.query(models.Restaurant).first()
    if not restaurants:
        f = open("restaurant_list.json",)
        restaurants = json.load(f)
        for restaurant in restaurants:
            restaurant = restaurant["properties"]
            if "name" not in restaurant:
                continue

            new_restaurant = models.Restaurant(
                                name=restaurant["name"],
                                cuisine = restaurant.get("cuisine", None),
                                take_away = restaurant.get("take_away", None),
                                email = restaurant.get("email", None),
                                indoor_seating = restaurant.get("indoor_seating" , None),
                                level = restaurant.get("level", None),
                                opening_hours = restaurant.get("opening_hours", None),
                                outdoor_seating = restaurant.get("outdoor_seating", None),
                                payment_mastercard = restaurant.get("payment:mastercard", None),
                                payment_visa = restaurant.get("payment:visa", None),
                                phone = restaurant.get("phone", None),
                                website = restaurant.get("website", None),
                                wheelchair = restaurant.get("wheelchair", None),
                                smoking = restaurant.get("smoking", None),
                                diet_vegan = restaurant.get("diet:vegan", None),
                                diet_vegetarian = restaurant.get("diet:vegetarian", None))
            db.add(new_restaurant)
        db.commit()
    


# Dependency

class RestaurantTags(str, Enum):
    vegan = "Vegan"
    vegetarian = "Vegetarian"
    asian = "Asian"
    italian = "Italian"
    vietnamese = "Vietnamese"
    korean = "Korean"
    mexican = "Mexican"



@app.get("/")
async def home(req: Request, db: Session = Depends(get_db)):
    restaurants = db.query(models.Restaurant).all()
    return templates.TemplateResponse("base.html",
                                      {"request": req, "restaurant_list": restaurants})



@app.post("/add")
def add(
    req: Request,
    name: str = Form(...),
    cuisine: str = Form(...),
    take_away: str = Form(...),
    # email: str = Form(...),
    indoor_seating: str = Form(...),
    # level: str = Form(...),
    opening_hours: str = Form(...),
    # outdoor_seating: str = Form(...),
    # payment_mastercard: str = Form(...),
    # payment_visa: str = Form(...),
    # phone: str = Form(...),
    # website: str = Form(...),
    # wheelchair: str = Form(...),
    # smoking: str = Form(...),
    # diet_vegan: str = Form(...),
    # diet_vegetarian: str = Form(...),
    db: Session = Depends(get_db)
):
    new_restaurant =  models.Restaurant(
                                name = name,
                                cuisine = cuisine,
                                take_away = take_away,
                                # email = email,
                                indoor_seating = indoor_seating,
                                # level = level,
                                opening_hours = opening_hours,
                                # outdoor_seating = outdoor_seating,
                                # payment_mastercard = payment_mastercard,
                                # payment_visa = payment_visa,
                                # phone = phone,
                                # website = website,
                                # wheelchair = wheelchair,
                                # smoking = smoking,
                                # diet_vegan = diet_vegan,
                                # diet_vegetarian = diet_vegetarian
                            )
    db.add(new_restaurant)
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


# @app.get("/update/{restaurant_id}")
# def update(req: Request, restaurant_id: int, db: Session = Depends(get_db)):
#     restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
#     restaurant.complete = not restaurant.complete
#     db.commit()
#     url = app.url_path_for("home")
#     return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/delete/{restaurant_id}")
def delete(req: Request, restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    db.delete(restaurant)
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)



@app.get("/random_restaurant")
def get_random_restaurant(req: Request, db: Session = Depends(get_db)):
    selected_restaurant = choice(db.query(models.Restaurant).all())
    return selected_restaurant



@app.get("/all_restaurants")
def get_random_restaurant(req: Request, db: Session = Depends(get_db)):
    return db.query(models.Restaurant).all()
