import requests
import os
from dotenv import load_dotenv

def main():
    print_header()
    load_dotenv()

    API_KEY = os.getenv("SPOONACULAR_API_KEY")

    URL = "https://api.spoonacular.com/recipes/complexSearch"


    while True:
        user_dish = input("(1) What dish are you looking for: ")
        diet = input("(2) Do you have any dietary restrictions \n\t\t"
                     "(eg. 1. vegan, 2.vegetarian, 3. keto, 4. leave blank or 5. other) : ")
        diet_no = ""
        while True:
            diet = input("(2) Do you have any dietary restrictions \n\t\t"
                         "(eg. 1. vegan, 2.vegetarian, 3. keto, 4. leave blank or 5. other) : ")
            if diet == "1":
                diet_no = "vegan"
                break
            elif diet == "2":
                diet_no = "vegetarian"
                break
            elif diet == "3":
                diet_no = "keto"
                break
            elif diet == "4":
                diet_no = "leave blank"
                break
            elif diet == "5":
                diet_no = input("Please enter the correct dietary restriction:")
                break
            else:
                print("something went wrong. Try again")


        paramaters = {
            "apiKey": API_KEY,
            "query": user_dish,
            "number": 3,
            "diet": diet
        }

        print("\nConnecting to Spoonacular API...")
        responses = requests.get(URL, params=paramaters)

        if responses.status_code == 200:
            print("Connection is successful!!\n")
            dishes = responses.json()
            recipie_list = dishes.get("results", [])

            print(f"We have found {len(recipie_list)} recipies for the dish: {user_dish}\n")

            for dish in recipie_list:
                title = dish["title"]
                recipe_id = dish["id"]
                image_url = dish["image"]
                print(f"🍴 {title} - ID: {recipe_id}")
                print(f"   Image: {image_url}")
        else:
            print(f"❌ Something went wrong. Error code: {responses.status_code}")
            print(responses.text)


        if len(recipie_list) == 0:
            print("\nNo recipies were found. Please try again.\n")
            continue

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
            full_data = recipie_response.json()
            print(full_data["title"])
            inter_list = full_data.get("analyzedInstructions", [])
            ingredients = full_data.get("extendedIngredients", [])
            if len(inter_list) > 0:
                print("Here's the ingredients:")
                count = 0
                for item in ingredients:
                    count+=1
                    print(f" {count}.{item["nameClean"]}")
                steps = inter_list[0]["steps"]
                for item in steps:
                    print(f"Step {item['number']}: {item['step']}")
            else:
                print("We don't have any steps for this recipe")

        else:
            print(f"Something went wrong. Error code: {recipie_response.status_code}")
            print(recipie_response.text)

        next_step = input("Do you want to look up another recipe? (y/n): ")
        if next_step == "n":
            print_footer()
            break

def print_header():
    print("\n" + "="*51)
    text = "Welcome to Flavor Finder!"
    print(f" {text.center(50, "-")}")
    print("="*51)

def print_footer():
    print("\n" + "=" * 51)
    text = "Thank you for using Flavor Finder!\n Hope to see you again"
    print(f" {text.center(50, "-")}")
    print("=" * 51)

main()