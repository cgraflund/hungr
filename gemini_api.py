import requests
import os
import json
import re

from models import RecommendationsResponse

GEMINI_ENDPOINT = os.getenv("GEMINI_ENDPOINT")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def clean_llm_text(text: str) -> str:
    """
    Strip ```json ... ``` or ``` ... ```
    """
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text

def parse_gemini_response(response) -> RecommendationsResponse:
    try:
        text_output = response["candidates"][0]["content"]["parts"][0]["text"]
        clean_text = clean_llm_text(text_output)

        return RecommendationsResponse(**json.loads(clean_text))
    except Exception as e:
        print("Failed to parse response:", e)
        return {"recommendations": []}

def get_recommendations(user_profile, restaurants):
    likes = user_profile.get("likes", "")
    dislikes = user_profile.get("dislikes", "")

    restaurant_text = "\n".join(
        [f"- {r['name']} (Rating: {r.get('rating')}, Types: {', '.join(r.get('types', []))}, Address: {r.get('address')})"
         for r in restaurants]
    )

    prompt = f"""
    You are a world-renowned food critic who writes with authority and precision. 
    Your role is to help a foodie find restaurants that match their preferences. 
    Base your recommendations on both the user’s profile and the list of nearby restaurants.

    The user likes: {likes}.
    The user dislikes: {dislikes}.

    Here is a list of nearby restaurants with their details:
    {restaurant_text}

    For each recommended restaurant:
    - "restaurant_name" must exactly match the name provided in the list.
    - "public_rating" must come directly from the provided Google Maps rating (use null if missing).
    - "personal_rating" is your own 1–10 score based on how well the restaurant aligns with the user’s likes and dislikes.
    - "description" is a general unbiased description of the restaurant 
    - "recommendation_reasoning" is a short descrtiption of why you think the user would like this restaruant.

    Return ONLY a JSON object with the following schema, nothing else:

    {{
    "recommendations": [
        {{
        "restaurant_name": "string",
        "public_rating": number,
        "personal_rating": number,
        "description": "string",
        "reccomendation_reasoning": "string"
        }}
    ]
    }}
    """

    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    body = {"contents": [{"parts": [{"text": prompt}]}]}

    response = requests.post(GEMINI_ENDPOINT, headers=headers, params=params, json=body)

    parsed_response = parse_gemini_response(response.json())

    return parsed_response
