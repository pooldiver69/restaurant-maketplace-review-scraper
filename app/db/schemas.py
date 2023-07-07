from pydantic import BaseModel


class OrderRatingBase(BaseModel):
    order: str
    rating: int
    restaurant_id: int
    review_id: int

class OrderRatingCreate(OrderRatingBase):
    pass


class OrderRating(OrderRatingBase):
    id: int
    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    reviewer: str
    date: str  
    review: str
    rating: int
    source: str
    restaurant_id: int
    new: bool = True

class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
    # orders: list[OrderRating] = []
    class Config:
        orm_mode = True


class RestaurantBase(BaseModel):
    name: str
    gh_url: str | None = None
    dd_url: str | None = None
    ue_url: str | None = None


class RestaurantCreate(RestaurantBase):
    pass

class Restaurant(RestaurantBase):
    id: int
    # reviews: list[Review] = []

    class Config:
        orm_mode = True
