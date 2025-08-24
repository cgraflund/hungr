import requests
import os
from models import Restaurant

GOOGLE_MAPS_API_URL = os.getenv("GOOGLE_MAPS_API_URL")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def get_restaurants_nearby(location, radius=1500, keyword="restaurant") -> list[Restaurant]:
    """
    location = "40.7128,-74.0060" (lat,lng)
    radius = meters (default: 1500m ~ 1 mile)
    """
    params = {
        "key": GOOGLE_MAPS_API_KEY,
        "location": location,
        "radius": radius,
        "keyword": keyword,
        "type": "restaurant"
    }
    response = requests.get(GOOGLE_MAPS_API_URL, params=params)
    data = response.json()
    results = []
    for place in data.get("results", []):
        results.append( Restaurant(name=place.get("name"), rating=place.get("rating"), address=place.get("vicinity"), types=place.get("types")))
       
    return results
