from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import func

async def create_restaurant(db: Session, restaurant: schemas.RestaurantCreate):
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.name == restaurant.dict().get('name')).first()
    if not db_restaurant:
        db_restaurant = models.Restaurant(**restaurant.dict())
        db.add(db_restaurant)
        db.commit()
        db.refresh(db_restaurant)
        return db_restaurant
    return None

async def get_all_restaurants(db: Session):
    return db.query(models.Restaurant).all()

async def get_restaurant_by_id(db: Session, id: int):
    return db.query(models.Restaurant).filter(models.Restaurant.id == id).first()

async def get_reviews_by_restaurant_id(db: Session, id: int):
    # print(db.query(models.Review)
    #       .join(models.OrderRating, models.OrderRating.review_id == models.Review.id)
    #       .group_by(models.Review.id)
    #       .filter(models.Review.restaurant_id == id))
    return db.query(models.Review).filter(models.Review.restaurant_id == id).all()

async def create_review(db: Session, review: schemas.ReviewCreate):
    stmt = (
        insert(models.Review)
        .values(**review.dict())
        .on_conflict_do_nothing(index_elements=[models.Review.reviewer, models.Review.date])
    )
    
    col = db.execute(stmt)
    db.flush()
    db.commit()
    return col

async def create_orderRating(db: Session, orderRating: schemas.OrderRatingCreate):
    db_orderRating = models.OrderRating(**orderRating.dict())
    db.add(db_orderRating)
    db.commit()
    db.refresh(db_orderRating)
    return db_orderRating

async def get_insights_by_restaurant_id(db: Session, id: int):
    most_popular_item = db.query(models.OrderRating).filter(models.OrderRating.restaurant_id == id).group_by(models.OrderRating.order).order_by(func.count().desc()).first()
    most_loved_item = db.query(models.OrderRating).filter(models.OrderRating.restaurant_id == id).group_by(models.OrderRating.order).order_by(func.sum(models.OrderRating.rating).desc()).first()
    least_loved_item = db.query(models.OrderRating).filter(models.OrderRating.restaurant_id == id).group_by(models.OrderRating.order).order_by(func.sum(models.OrderRating.rating).asc()).first()
    res = {
        "most_popular_item": most_popular_item.order if most_popular_item else None,
        "most_loved_item": most_loved_item.order if most_loved_item else None,
        "least_loved_item": least_loved_item.order if least_loved_item else None
    }
    return res
