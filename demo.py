from src.db import init_db, get_user, bulk_add_users
from src.google_maps_api import get_restaurants_nearby
from src.gemini_api import get_recommendations


def run_demo():
    # Get user preferences
    user_dict = dict()
    for user_key in ["Connor", "Veronica", "Kennedy", "Jonathan", "Amy", "Kaitlyn", "Jordan", "Cody"]:
        user_dict[user_key] = get_user(user_key)

    location = "39.745154503926216, -104.98128501283851"
    restaurants = get_restaurants_nearby(location)

    group_permutations = [["Connor", "Veronica"]] #, ["Connor", "Kennedy", "Jonathan"], ["Connor", "Veronica", "Kaitlyn", "Amy", "Caleb"]]

    for group in group_permutations:
        print(f"Getting recommendations near {location} for group {group}...")

        group_users = [user_dict[name] for name in group if name in user_dict]
        # Get AI recommendations
        recommendations = get_recommendations(group_users, restaurants)

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
