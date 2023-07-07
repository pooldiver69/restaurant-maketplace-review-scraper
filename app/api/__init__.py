from fastapi import APIRouter, Request, Response
from app.db import schemas, crud
import traceback
from app.utils.gh_scraper import gh_scraper
router = APIRouter(
    responses={404: {"err": "Not found"}}
)

@router.get('/restaurants', response_model=list[schemas.Restaurant])
async def get_restaurants(request: Request):
    try:
        data = await crud.get_all_restaurants(db=request.app.db)
        return data
    except Exception as ex:
        return Response(str(ex), 500)

async def insert_reviews_and_orderRating_helper(data, db):
    for review in data:
        review['review'] = review['review'].encode('utf-8', 'ignore').decode('utf-8', 'ignore')
        db_review = await crud.create_review(db=db, review=schemas.ReviewCreate(
            **review
        ))
        if db_review.inserted_primary_key[0] != 0:
            review_id = db_review.inserted_primary_key[0]
            for order in review.get('orders', []):
                try:
                    await crud.create_orderRating(db=db, orderRating=schemas.OrderRatingCreate(
                        **{
                            "order": order,
                            "rating": review.get('rating', 0),
                            "restaurant_id": review.get('restaurant_id'),
                            "review_id": review_id
                        }
                    )) 
                except:
                    traceback.print_exc()

@router.get('/scrape/restaurant/{id}')
async def scrape_restaurant(request: Request, id: int):
    try:
        restaurant = await crud.get_restaurant_by_id(db=request.app.db, id=id)
        if not restaurant: return Response("restaurant not exists", 404)
        data = gh_scraper(restaurant.gh_url, id) if restaurant.gh_url else []
        await insert_reviews_and_orderRating_helper(data, request.app.db)
        return "ok"
    except Exception as ex:
        traceback.print_exc()
        return Response(str(ex), 500)

@router.get('/restaurant/{id}/reviews', response_model=list[schemas.Review])
async def get_restaurant_reviews_by_id(request: Request, response: Response, id:int):
    try:
        data =  await crud.get_reviews_by_restaurant_id(db=request.app.db, id=id)
        return data
    except Exception as ex:
        response.status_code = 500
        return {"err": str(ex)}

@router.get('/restaurant/{id}/insights')
async def get_restaurant_insights_by_id(request: Request, response: Response, id:int):
    try:
        data =  await crud.get_insights_by_restaurant_id(db=request.app.db, id=id)
        return data
    except Exception as ex:
        response.status_code = 500
        return {"err": str(ex)}
    