from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google_maps_api import get_restaurants_nearby
from gemini_api import get_recommendations
from db import get_all_users, init_db, bulk_add_users
from models import RecommendationRequest

app = FastAPI()

# Allow your frontend origin
origins = [
    "http://localhost:8080",  # your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # allow frontend
    allow_credentials=True,
    allow_methods=["*"],        # allow all HTTP methods
    allow_headers=["*"],        # allow all headers
)

@app.get("/users")
def list_users():
    """Return all users in the database."""
    return [user.name for user in get_all_users()]

@app.post("/recommendations")
def recommend(req: RecommendationRequest):
    """Get recommendations for a group of users and a location."""
    user_dict = {u.name: u for u in get_all_users()}
    group_users = [user_dict[name] for name in req.users if name in user_dict]

    restaurants = get_restaurants_nearby(req.location)
    recommendations = get_recommendations(group_users, restaurants)
    print(recommendations)
    return recommendations
