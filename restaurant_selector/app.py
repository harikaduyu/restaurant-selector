import logging
from random import randint
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


def set_up_database(db : SessionLocal = None):
    f = open("restaurant_list.json",)
    restaurants = json.load(f)
    for restaurant in restaurants:
        restaurant = restaurant["properties"]
        if "name" not in restaurant:
            continue
        name = restaurant["name"]
        logger.debug(f"NAME = {name}")
        logger.debug(restaurant)
        email = restaurant["email"]

        # new_restaurant = models.Restaurant(
        #                     name=restaurant["name"],
        #                     cuisine = restaurant["cuisine"]
        #                     take_away = restaurant.get("take_away", None)
        #                     email = restaurant.get("email", None)
        #                     indoor_seating = 
        #                     level = 
        #                     opening_hours = 
        #                     outdoor_seating = 
        #                     payment_mastercard = 
        #                     payment_visa = 
        #                     phone = 
        #                     website = 
        #                     wheelchair = 
        #                     smoking = 
        #                     diet_vegan = 
        #                     diet_vegetarian = 
        # db.add(new_restaurant)
    # db.commit()
    

set_up_database()

def get_db():
    db = SessionLocal()
    try:
        restaurants = db.query(models.Restaurant).all()
        if not restaurants:
            set_up_database(db)
        yield db
    finally:
        db.close()



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
    f = open("restaurant_list.json",)
    restaurants = json.load(f)

    return templates.TemplateResponse("base.html",
                                      {"request": req, "restaurant_list": restaurants})



@app.post("/add")
def add(req: Request,
        title: str = Form(...),
        emoji: str = Form(...),
        tags: List[str] = Form(...),
        # tags: List[str] = Form(...),
        db: Session = Depends(get_db)
):
    logger.info(f"req {req}")
    logger.info(f"tags {tags}")
    logger.info(f"emoji {emoji}")
    new_restaurant = models.Restaurant(title=title, emoji=emoji, tags=", ".join(tags))
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
    f = open("restaurant_list.json",)
    restaurants = json.load(f)
    if restaurants:
        random_index = randint(0,len(restaurants)-1)
        selected_restaurant =  restaurants[random_index]["properties"]
    return selected_restaurant



@app.get("/all_restaurants")
def get_random_restaurant(req: Request, db: Session = Depends(get_db)):
    f = open("restaurant_list.json",)
    restaurants = json.load(f)

    return restaurants
