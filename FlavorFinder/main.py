import requests
import os
from dotenv import load_dotenv
import random


def main():
    print_header()
    load_dotenv()
    API_KEY = os.getenv("SPOONACULAR_API_KEY")
    URL = "https://api.spoonacular.com/recipes/complexSearch"

    while True:
        print("\n************ Let's look at the choices ************")
        print("1. Search")
        print("2. Favorites")
        print("3. Random recipies")
        print("4. Saved recipies")
        print("5. Quit")
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
                    recipie_list = response.json().get("results", [])
                    if not recipie_list:
                        print("No recipes found.")
                        continue

                    for dish in recipie_list:
                        print(f"🍴 {dish['title']} - ID: {dish['id']}")

                    selected_id = input("\nType the ID to see the full recipe: ")

                    info_url = f"https://api.spoonacular.com/recipes/{selected_id}/information"
                    info_resp = requests.get(info_url, params={"apiKey": API_KEY})

                    if info_resp.status_code == 200:
                        data = info_resp.json()
                        print(f"\n--- {data['title']} ---")
                        for i, ing in enumerate(data.get("extendedIngredients", []), 1):
                            print(f"{i}. {ing.get('nameClean', ing['name'])}")

                        print("\ninstructions:")
                        instructions = data.get("analyzedInstructions")
                        if instructions:
                            for step in instructions[0]["steps"]:
                                print(f"{step['number']}. {step['step']}")
                        else:
                            print("No instructions found.")

                        # Save logic
                        save = input("\nSave to favorites? (y/n): ")
                        if save.lower() == "y":
                            with open("favorite.txt", "a") as f:
                                f.write(data["title"] + "\n")

                        data_written = "recipes.txt"

                        with open(data_written, "w") as file:
                            file.write(data["title"])
                            file.write("\n")
                            for instruction in data["instructions"]:
                                file.write(instruction)

                else:
                    print(f"Error: {response.status_code}")

            elif first_choice == "2":
                print("\n" + "*" * 30)
                print("      YOUR FAVORITES      ")
                print("*" * 30)
                if os.path.exists("favorite.txt"):
                    with open("favorite.txt", "r") as f:
                        print(f.read())
                else:
                    print("No favorites saved yet!")

            elif first_choice == "3":
                print("\n" + "*" * 30)
                print("Let's create a random recipie for you!!")
                print("\nConnecting to Spoonacular...")

                parameters = {
                    "apiKey": API_KEY,
                    "number": 1,
                }

                response = requests.get("https://api.spoonacular.com/recipes/random", params=parameters)
                data = response.json()['recipes'][0]

                print(f"{data["title"] } - ID: {data['id']}")
                save = input("\n Do you want to add this to your recipies? (y/n): ")

                if save == "y":
                    with open("recipes.txt", "a") as f:
                        f.write(data["title"] + "\n")

                fav = input("\nDo you want to add this to your favorites? (y/n): ")

                if fav == "y":
                    with open("favorite.txt", "a") as f:
                        f.write(data["title"] + "\n")


            elif first_choice == "4":
                print("\n" + "*" * 30)
                print("      YOUR RECIPES      1")
                print("*" * 30)

            elif first_choice == "5":
                print_footer()
                break

        except ValueError:
            print("Please enter a valid number (1, 2, or 3).")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


def print_header():
    print("\n" + "=" * 51)
    text = "Welcome to Flavor Finder!"
    print(f" {text.center(50, '-')}")
    print("=" * 51)


def print_footer():
    print("\n" + "=" * 51)
    text = "Thank you for using Flavor Finder!"
    print(f" {text.center(50, '-')}")
    print("=" * 51)

def add_favorites(info):
    file = "favorites.txt"

    with open(file, "a") as f:
        f.write(info)

def add_to_recipes(info):
    file = "recipes.txt"

    with open(file, "a") as f:
        f.write(info)

def get_recipes(info):
    if os.path.exists("recipes.txt"):
        with open("recipes.txt", "r") as f:
            print(f.read())

def get_favorites(info):
    if os.path.exists("favorites.txt"):
        with open("favorites.txt", "r") as f:
            print(f.read())

if __name__ == "__main__":
    main()