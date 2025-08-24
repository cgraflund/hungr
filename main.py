from db import init_db, add_user, get_user
from google_maps_api import get_restaurants_nearby
from gemini_api import get_recommendations

def run_demo():
    # Initialize DB
    init_db()

    # Add user if not exists
    add_user("Connor", likes="sushi, vegetarian, falafel", dislikes="beef")

    # Get user preferences
    user_profile = get_user("Connor")

    # Fetch restaurants near a location (example: NYC lat/lng)
    location = "40.7128,-74.0060"
    restaurants = get_restaurants_nearby(location)

    # Get AI recommendations
    recommendations = get_recommendations(user_profile, restaurants)

    print("\nHere are some restaurant recommendations for you:\n")

    for i, rec in enumerate(recommendations.recommendations, start=1):
        print(f"{i}. {rec.restaurant_name}")
        print(f"   - Public Rating: {rec.public_rating if rec.public_rating is not None else 'N/A'}")
        print(f"   - Description: {rec.description}")
        print(f"   - Personal Rating: {rec.personal_rating}/10")
        print(f"   - Why you'd like it: {rec.reccomendation_reasoning}")
        print("")  # Blank line for spacing

if __name__ == "__main__":
    run_demo()
