import logging
from random import randint
from enum import Enum
from typing import List

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


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class RestaurantTags(str, Enum):
    vegan = "Vegan"
    vegetarian = "Vegetarian"
    asian = "Asian"
    italian = "Italian"
    vietnamese = "Vietnamese"
    korean = "Korean"
    mexican = "Mexican"

@app.get("/")
async def choose_restaurant(req: Request, db: Session = Depends(get_db)):
    restaurants = db.query(models.Restaurant).all()
    selected_restaurant = {}
    if restaurants:
        # random_index = randint(0,len(restaurants)-1)
        random_index = -1
        selected_restaurant =  restaurants[random_index]

    return selected_restaurant




@app.get("/add_restaurant")
async def home(req: Request, db: Session = Depends(get_db)):
    restaurants = db.query(models.Restaurant).all()
    return templates.TemplateResponse("base.html",
                                      {"request": req, "restaurant_list": restaurants, 'tags': [e.value for e in RestaurantTags]})



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
