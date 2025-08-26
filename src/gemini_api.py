import requests
import os
import json
import re

from models import Recommendation, User, Restaurant

GEMINI_ENDPOINT = os.getenv("GEMINI_ENDPOINT")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def clean_llm_text(text: str) -> str:
    """
    Strip ```json ... ``` or ``` ... ```
    """
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text

def parse_gemini_response(response) -> list[Recommendation]:
    try:
        text_output = response["candidates"][0]["content"]["parts"][0]["text"]
        clean_text = clean_llm_text(text_output)

        # Parse JSON array
        recommendations_list = json.loads(clean_text)

        # Validate each entry as a Recommendation object
        return [Recommendation(**rec) for rec in recommendations_list]
    except Exception as e:
        print("Failed to parse response:", e)
        return {"recommendations": []}
    


def get_recommendations(users: list[User], restaurants: list[Restaurant]):
    user_profiles_text = "\n".join(
        [
            f"- {u.name} (Likes: {u.likes}; Dislikes: {u.dislikes})"
            for u in users
        ]
    )

    restaurant_text = "\n".join(
        [f"- {r.name} (Rating: {r.rating}, Types: {', '.join(r.types)}, Address: {r.address})"
         for r in restaurants]
    )

    prompt = f"""
        You are a world-renowned food critic tasked with finding the best restaurant for a group of friends
        with different tastes. Each person has their own likes and dislikes, and your job is to combine their
        preferences into a shared taste profile that maximizes group satisfaction.

        Group of friends:
        {user_profiles_text}

        Nearby restaurants:
        {restaurant_text}

        Please:
        1. Analyze everyone's likes and dislikes to build a shared group taste profile.
        2. Select the top 3 restaurants that best balance the group's tastes.
        3. Output ONLY in the following JSON schema, where "public_rating" is taken from the restaurant's info
        and "personal_rating" is your critic score of how well it matches the group (scale 1–10).

        Return ONLY a JSON array of objects with the following schema, nothing else:

        [
            {{
                "restaurant_name": "string",
                "public_rating": number,
                "personal_rating": number,
                "description": "string",
                "reccomendation_reasoning": "string"
            }}
        ]
    """


    response_schema = {
        "type": "ARRAY",
        "items": {
            "type": "OBJECT",
            "properties": {
                "restaurant_name": {"type": "STRING"},
                "public_rating": {"type": "NUMBER"},
                "personal_rating": {"type": "NUMBER"},
                "description": {"type": "STRING"},
                "reccomendation_reasoning": {"type": "STRING"}
            },
            "propertyOrdering": ["restaurant_name", "public_rating", "personal_rating", "description", "reccomendation_reasoning"]
        }
    }

    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": response_schema
        }
    }

    response = requests.post(GEMINI_ENDPOINT, headers=headers, params=params, json=body)

    print(response.json())

    parsed_response = parse_gemini_response(response.json())

    return parsed_response
