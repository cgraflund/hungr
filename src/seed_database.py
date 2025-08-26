from db import bulk_add_users, init_db

def seed_database():
    users = [
        {"name": "Connor", "likes": "Sushi, thai, pasta", "dislikes": "Red Meat"},
        {"name": "Veronica", "likes": "Sushi, ramen, fresh seafood", "dislikes": "Olives, bell peppers, eggplant"},
        {"name": "Kennedy", "likes": "BBQ, fried chicken, hearty comfort food", "dislikes": "Raw fish"},
        {"name": "Jonathan", "likes": "Vegan bowls, falafel, Mediterranean", "dislikes": "Red meat"},
        {"name": "Amy", "likes": "Italian pasta, pizza, wine", "dislikes": "Seafood"},
        {"name": "Kaitlyn", "likes": "Burgers, Mexican food, tacos", "dislikes": "Indian curries"},
        {"name": "Jordan", "likes": "Thai food, pad thai, dumplings", "dislikes": "Cheese"},
        {"name": "Cody", "likes": "Breakfast food, biscuits and gravy", "dislikes": "Fish, mushrooms"},
    ]

    bulk_add_users(users)

if __name__ == "__main__":
    init_db()
    seed_database()
    print("Database initialized and users seeded successfully!")
