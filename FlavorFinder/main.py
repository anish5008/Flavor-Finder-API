import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SPOONACULAR_API_KEY")

URL = "https://api.spoonacular.com/recipes/complexSearch"

user_dish = input("What dish are you looking for: ")

paramaters = {
    "apiKey": API_KEY,
    "query": user_dish,
    "number": 3
}

print("Connecting to Spoonacular API...")
responses = requests.get(URL, params=paramaters)

if responses.status_code == 200:
    print("Connection is successful!")
    dishes = responses.json()
    recipie_list = dishes.get("result", [])

    print(f"We have found {len(recipie_list)} recipies for the dish: {user_dish}")

    for dish in recipie_list:
        title = dish["title"]
        recipe_id = dish["id"]
        image_url = dish["image"]
        print(f"🍴 {title} - ID: {recipe_id}")
        print(f"   Image: {image_url}")
else:
    print(f"❌ Something went wrong. Error code: {responses.status_code}")
    print(responses.text)
