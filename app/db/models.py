from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    gh_url = Column(String, unique=True)
    dd_url = Column(String, unique=True)
    ue_url = Column(String, unique=True)

    reviews = relationship("Review", back_populates="restaurant")
    orders =  relationship("OrderRating", back_populates="restaurant")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    reviewer = Column(String, index=True)
    date = Column(String, index=True)
    review = Column(String, index=True)
    rating = Column(Integer, index=True)
    source = Column(String, index=True)
    new = Column(Boolean, index=True, default=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))

    __table_args__ = (UniqueConstraint("reviewer", "date", name="uniq_reviewer_in_same_date"),)

    restaurant = relationship("Restaurant", back_populates="reviews")
    orders = relationship("OrderRating", back_populates="review")

class OrderRating(Base):
    __tablename__ = "orderRatings"

    id = Column(Integer, primary_key=True, index=True)
    order = Column(String, index=True)
    rating = Column(Integer, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    review_id = Column(Integer, ForeignKey("reviews.id"))

    restaurant = relationship("Restaurant", back_populates="orders")
    review = relationship("Review", back_populates="orders")