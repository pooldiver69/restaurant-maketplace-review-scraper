from fastapi import Depends, FastAPI, Request, Response
from sqlalchemy.orm import Session
from fastapi_utils.tasks import repeat_every
from app.api import router

from app.db import crud, models, schemas
from app.db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup_event(db:Session= next(get_db())):
    app.db = db
    await crud.create_restaurant(db=db, restaurant=schemas.RestaurantCreate(
        name="Napoli Pizza", 
        gh_url="https://www.grubhub.com/restaurant/napoli-pizza-1045-polk-st-san-francisco/2058686"
    ))

@app.get('/')
async def hello():
    return {"msg": "Hello World"}

from .api import insert_reviews_and_orderRating_helper
from .utils.gh_scraper import gh_scraper

async def fetch_scrape_all_restaurants(db:Session= next(get_db())) -> None:
    print('refresh!')
    restaurants = await crud.get_all_restaurants(db=db)
    for restaurant in restaurants:
        data = gh_scraper(restaurant.gh_url, restaurant.id) if restaurant.gh_url else []
        await insert_reviews_and_orderRating_helper(data, db)
    return 

@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)  # 24 hour
async def remove_expired_tokens_task() -> None:
    await fetch_scrape_all_restaurants()