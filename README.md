# 🍽️ Hungr

Hungr is a fun web tool that helps groups of friends decide where to eat.  
It combines everyone’s food likes and dislikes, finds nearby restaurants, and uses an AI food critic to recommend the top spots for maximum group satisfaction.

---

## 🚀 Features

- Add multiple users with their food preferences (likes and dislikes).
- Fetch nearby restaurants from your current location.
- AI-powered restaurant critic that:
  - Builds a shared taste profile for the group.
  - Picks the top 3 restaurants.
  - Explains the reasoning behind the recommendations.
- Clean React frontend with Tailwind styling.

---

## 🧩 Components

### Backend

- **FastAPI Server**  
  Handles API requests, connects to the database, and sends user/restaurant data to the AI model.
- **Database (SQLite)**  
  Stores user profiles with likes and dislikes.  
  Includes a seed script to pre-populate the database with sample users.
- **Recommendation Engine**  
  Formats prompts for the AI model, validates responses against a strict schema, and returns restaurant recommendations.

### Frontend

- **React App**
  - User selector (checkbox list for group members).
  - Auto-fetches current geolocation to find restaurants near you.
  - Displays top 3 AI-chosen restaurants with ratings and reasoning.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/restaurant-picker.git
cd restaurant-picker
```

### 2. Copy .env and setup api keys

1. Make a copy of sample.env and rename to .env
2. Create a google cloud account and setup the google maps and gemini apis to get api keys
3. Add `GOOGLE_MAPS_API_KEY` and `GEMINI_API_KEY` to the .env file

### 3. Run everything

`make run`
