import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SPOONACULAR_API_KEY")

URL = "https://api.spoonacular.com/recipes/complexSearch"

user_dish = input("What dish are you looking for: ")
diet = input("Do you have any dietary restrictions (eg. vegan, vegetarian, keto or leave blank) : ")

paramaters = {
    "apiKey": API_KEY,
    "query": user_dish,
    "number": 3,
    "diet": diet
}

print("Connecting to Spoonacular API...")
responses = requests.get(URL, params=paramaters)

if responses.status_code == 200:
    print("Connection is successful!")
    dishes = responses.json()
    recipie_list = dishes.get("results", [])

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

print("Choose one of the given dishes to read through the recipie!!")
selected_id = input("Type in the ID for the selected dish: ")

recipie_url = f"https://api.spoonacular.com/recipes/{selected_id}/information"

recipie_param = {
    "apiKey": API_KEY,
    "query": user_dish,
    "number": 3,
    "diet": diet
}
recipie_response = requests.get(recipie_url, params=recipie_param)

if recipie_response.status_code == 200:
    recipie = recipie_response.json()
    recipe = recipie["analyzedInstructions"]
    ingredients = recipe["ingredients"]
    steps = recipe["steps"]
    print(f"The recipe title is {recipe["name"]}")
    print(f"The recipe ingredients is {ingredients}")
    print(f"The recipe steps is {steps}")
else:
    print(f"Something went wrong. Error code: {recipie_response.status_code}")
    print(recipie_response.text)
    