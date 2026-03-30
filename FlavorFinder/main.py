import requests
import os
from dotenv import load_dotenv
import random

load_dotenv()
API_KEY = os.getenv("SPOONACULAR_API_KEY")
URL = "https://api.spoonacular.com/recipes/complexSearch"

def main():
    cart = "shopping_cart.txt"
    data_written = "recipes.txt"
    fav_file = "favorite.txt"

    print_header()

    if not API_KEY:
        print("\n🔑 API Key not found in .env file.")
        API_KEY = input("Please paste your Spoonacular API Key here: ").strip()

    while True:
        print("\n************ Let's look at the choices ************")
        print("1. Search by dish")
        print("2. Search by ingredients")
        print("3. Favorites")
        print("4. Random recipes")
        print("5. Saved recipes")
        print("6. View the shopping cart")
        print("7. Quit")
        print("***************************************************")

        try:
            first_choice = input("What feature would you like to utilize: ")

            if first_choice == "1":
                user_dish = input("What dish are you looking for? ")

                diet_no = ""
                diet = input("(2) Dietary restrictions (1.vegan, 2.vegetarian, 3.keto, 4.none, 5.other): ")
                if diet == "1":
                    diet_no = "vegan"
                elif diet == "2":
                    diet_no = "vegetarian"
                elif diet == "3":
                    diet_no = "keto"
                elif diet == "5":
                    diet_no = input("Enter restriction: ")

                num = int(input("Number of recipes to search: "))

                parameters = {
                    "apiKey": API_KEY,
                    "query": user_dish,
                    "number": num,
                    "diet": diet_no
                }

                print("\nConnecting to Spoonacular...")
                response = requests.get(URL, params=parameters)

                if response.status_code == 200:
                    recipe_list = response.json().get("results", [])
                    if not recipe_list:
                        print("No recipes found.")
                        continue

                    for dish in recipe_list:
                        print(f"🍴 {dish['title']} - ID: {dish['id']}")

                    selected_id = input("\nType the ID to see the full recipe: ")

                    info_url = f"https://api.spoonacular.com/recipes/{selected_id}/information"
                    info_resp = requests.get(info_url, params={"apiKey": API_KEY, "includeNutrition": True})

                    if info_resp.status_code == 200:
                        data = info_resp.json()
                        print(f"\n--- {data['title']} ---")
                        for i, ing in enumerate(data.get("extendedIngredients", []), 1):
                            print(f"{i}. {ing.get('nameClean', ing['name'])}")

                        print("\nInstructions:")
                        instructions = data.get("analyzedInstructions")
                        if instructions and len(instructions) > 0:
                            for step in instructions[0]["steps"]:
                                print(f"{step['number']}. {step['step']}")
                        else:
                            print("No instructions found.")

                        nutri = input("\nSee nutrition info? (y/n): ")
                        if nutri.lower() == "y":
                            get_nutrients(data)

                        add_to_shopping = input("\nWould you like to add ingredients to the shopping list (y/n)? ")
                        add_to_shopping_cart(add_to_shopping, data, cart)

                        save = input("\nSave to favorites? (y/n): ")
                        if save.lower() == "y":
                            add_favorites(data["title"] + "\n")

                        with open(data_written, "a") as file:
                            file.write(f"\nRecipe: {data['title']}\n")
                            file.write("Ingredients:\n")
                            for ing in data.get("extendedIngredients", []):
                                file.write(f"- {ing.get('original')}\n")
                else:
                    print(f"Error: {response.status_code}")

            elif first_choice == "2":
                ingredients = input("\nEnter your ingredients separated by commas: ")
                num = int(input("Number of recipes to search for: "))
                new_URL = "https://api.spoonacular.com/recipes/findByIngredients"

                parameters = {
                    "apiKey": API_KEY,
                    "ingredients": ingredients,
                    "number": num
                }

                ingResponse = requests.get(new_URL, params=parameters)

                if ingResponse.status_code == 200:
                    results = ingResponse.json()

                    for x in results:
                        print(f"{x['title']} - ID: {x['id']}")

                    selected_id = input("\nType the ID to see the full recipe: ")

                    info_url = f"https://api.spoonacular.com/recipes/{selected_id}/information"
                    info_resp = requests.get(info_url, params={"apiKey": API_KEY, "includeNutrition": True})

                    if info_resp.status_code == 200:
                        data = info_resp.json()
                        print(f"\n--- {data['title']} ---")
                        for i, ing in enumerate(data.get("extendedIngredients", []), 1):
                            print(f"{i}. {ing.get('nameClean', ing['name'])}")

                        print("\nInstructions:")
                        instructions = data.get("analyzedInstructions")
                        if instructions and len(instructions) > 0:
                            for step in instructions[0]["steps"]:
                                print(f"{step['number']}. {step['step']}")
                        else:
                            print("No instructions found.")

                        nutri = input("\nSee nutrition info? (y/n): ")
                        if nutri.lower() == "y":
                            get_nutrients(data)

                        add_to_shopping = input("\nWould you like to add the ingredients to the shopping list (y/n)? ")
                        add_to_shopping_cart(add_to_shopping, data, cart)

                        fav_choice = input("\nSave to favorites? (y/n): ")
                        if fav_choice.lower() == "y":
                            add_favorites(data["title"] + "\n")

                        with open(data_written, "a") as file:
                            file.write(f"\nRecipe: {data['title']}\n")
                            file.write("Ingredients:\n")
                            for ing in data.get("extendedIngredients", []):
                                file.write(f"- {ing.get('original')}\n")

            elif first_choice == "3":
                print("\n" + "*" * 30)
                print("      YOUR FAVORITES      ")
                print("*" * 30)
                get_favorites()

            elif first_choice == "4":
                print("\n" + "*" * 30)
                print("Let's create a random recipe for you!!")
                print("\nConnecting to Spoonacular...")

                parameters = {
                    "apiKey": API_KEY,
                    "number": 1,
                }

                response = requests.get("https://api.spoonacular.com/recipes/random", params=parameters)
                data = response.json()['recipes'][0]

                print(f"{data['title']} - ID: {data['id']}")
                save = input("\nDo you want to add this to your recipes? (y/n): ")

                if save.lower() == "y":
                    add_to_recipes(data["title"] + "\n")

                fav = input("\nDo you want to add this to your favorites? (y/n): ")

                if fav.lower() == "y":
                    add_favorites(data["title"] + "\n")

            elif first_choice == "5":
                print("\n" + "*" * 30)
                print("      YOUR RECIPES      ")
                print("*" * 30)
                get_recipes()

            elif first_choice == "6":
                print("\n" + "*" * 30)
                print("      YOUR SHOPPING CART      ")
                print("*" * 30)

                if os.path.exists(cart):
                    with open(cart, "r") as file:
                        print(file.read())
                else:
                    print("No items saved in the cart yet!")

            elif first_choice == "7":
                print_footer()
                break

        except ValueError:
            print("Please enter a valid number (1-7).")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def print_header():
    print("\n" + "=" * 51)
    text = "Welcome to Flavor Finder!\n You have to create a free API key from Spponacular to keep mine and you data safe. \n It takes less than 2 minutes"
    print(f" {text.center(50, '-')}")
    print("=" * 51)

def print_footer():
    print("\n" + "=" * 51)
    text = "Thank you for using Flavor Finder!"
    print(f" {text.center(50, '-')}")
    print("=" * 51)

def add_favorites(info):
    file = "favorite.txt"
    with open(file, "a") as f:
        f.write(info)

def add_to_recipes(info):
    file = "recipes.txt"
    with open(file, "a") as f:
        f.write(info)

def get_recipes():
    if os.path.exists("recipes.txt"):
        with open("recipes.txt", "r") as f:
            print(f.read())
    else:
        print("No recipes saved yet!")

def get_favorites():
    if os.path.exists("favorite.txt"):
        with open("favorite.txt", "r") as f:
            print(f.read())
    else:
        print("No favorites saved yet!")

def add_to_shopping_cart(ans, data, cart_path):
    if ans.lower() == "y":
        with open(cart_path, "a") as file:
            file.write(f"\n---------- {data['title']} ----------\n")
            for ing in data.get("extendedIngredients", []):
                file.write(f"- {ing.get('original')} \n")
            print("Finished adding ingredients to the shopping list.")

def get_nutrients(data):
    needed = input("Enter macros (e.g., Calories, Protein, Fat): ")
    user_macros = [m.strip().title() for m in needed.split(",")]
    api_nutrients = data.get("nutrition", {}).get("nutrients", [])

    print("\n--- Nutritional Results ---")
    for n in api_nutrients:
        if n.get("name") in user_macros:
            print(f"✅ {n['name']}: {n['amount']} {n['unit']}")

if __name__ == "__main__":
    main()