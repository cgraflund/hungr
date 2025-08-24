from pydantic import BaseModel, Field
from typing import List, Optional

class User(BaseModel):
    name: str = Field(..., description="User's name")
    likes: str = Field(..., description="User's preferred taste profile")
    dislikes: str = Field(..., description="What the user wants to avoid")

class Restaurant(BaseModel):
    name: str = Field(..., description="User's name")
    rating: float = Field(..., description="Restaurant's rating")
    address: str = Field(..., description="Address of the restaurant")
    types: list[str] = Field([], description="Types of cuisine")

class Recommendation(BaseModel):
    restaurant_name: str = Field(..., description="Name of the restaurant")
    public_rating: Optional[float] = Field(None, description="Google Maps rating of the restaurant")
    personal_rating: int = Field(..., ge=1, le=10, description="Personal rating for this user (1-10)")
    description: str = Field(..., description="General description of the restaurant")
    reccomendation_reasoning: str = Field(..., description="Why the user would like this restaurant")


class RecommendationsResponse(BaseModel):
    recommendations: List[Recommendation] = Field(..., description="List of restaurant recommendations")