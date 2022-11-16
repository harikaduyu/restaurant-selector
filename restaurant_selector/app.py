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
from restaurant_selector.helpers import update_restaurant_list

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
            # restaurant = restaurant["properties"]
            if "name" not in restaurant:
                continue
            address = restaurant.get('addr:street', '') + ' ' + \
                      restaurant.get('addr:housenumber', '') + ' ' + \
                      restaurant.get('addr:postcode', '') +  ' ' + \
                      restaurant.get('addr:city', '')
                      
            new_restaurant = models.Restaurant(
                                id = restaurant["id"],
                                name=restaurant["name"],
                                cuisine = restaurant.get("cuisine", '-'),
                                take_away = restaurant.get("takeaway", '-'),
                                email = restaurant.get("email", '-'),
                                indoor_seating = restaurant.get("indoor_seating" , '-'),
                                level = restaurant.get("level", '-'),
                                opening_hours = restaurant.get("opening_hours", '-'),
                                outdoor_seating = restaurant.get("outdoor_seating", '-'),
                                payment_mastercard = restaurant.get("payment:mastercard", '-'),
                                payment_visa = restaurant.get("payment:visa", '-'),
                                phone = restaurant.get("phone", '-'),
                                website = restaurant.get("website", '-'),
                                wheelchair = restaurant.get("wheelchair", '-'),
                                smoking = restaurant.get("smoking", '-'),
                                diet_vegan = restaurant.get("diet:vegan", '-'),
                                diet_vegetarian = restaurant.get("diet:vegetarian", '-'),
                                address = address)
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
    cuisine_list = []
    for restaurant in db.query(models.Restaurant.cuisine).distinct():
        logger.info(restaurant)
        cuisine_list.append(restaurant.cuisine)
    return templates.TemplateResponse("base.html",
                                      {"request": req, "restaurant_list": restaurants, "cuisine_list" : cuisine_list})



@app.post("/search")
def search(
    req: Request,
    name: str = Form(''),
    cuisine: str = Form(''),
    db: Session = Depends(get_db)
):

    if cuisine != '-':
        filter_query = models.Restaurant.cuisine == cuisine
    if name:
        filter_query =  models.Restaurant.name == name

    restaurants = db.query(models.Restaurant).filter(filter_query)
    cuisine_list = []
    for restaurant in db.query(models.Restaurant.cuisine).distinct():
        logger.info(restaurant)
        cuisine_list.append(restaurant.cuisine)
    return templates.TemplateResponse("base.html",
                                      {"request": req, "restaurant_list": restaurants, "cuisine_list" : cuisine_list})


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
def get_all_restaurant(req: Request, db: Session = Depends(get_db)):
    return db.query(models.Restaurant).all()



@app.get("/update_restaurants")
def update_restaurants(req: Request, db: Session = Depends(get_db)):
    logger.info("Updating restaurant list..")
    update_restaurant_list()
    logger.info("Finished updating restaurant list..")
    return "Finished updating restaurant list.."


@app.get("/show_random_restaurant")
def show_random_restaurant(req: Request, db: Session = Depends(get_db)):
    selected_restaurant = choice(db.query(models.Restaurant).all())

    return templates.TemplateResponse("restaurant_details.html",
                                      {"request": req, "restaurant": selected_restaurant})


@app.get("/show_restaurant/{restaurant_id}")
def show_restaurant_details(req: Request, restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()

    return templates.TemplateResponse("restaurant_details.html",
                                      {"request": req, "restaurant": restaurant})